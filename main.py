import os
from flask import Flask, request, send_file, render_template_string
from PIL import Image

def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pixels = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pixels[j] % 2 != 0):
                pixels[j] -= 1
            elif (datalist[i][j] == '1') and (pixels[j] % 2 == 0):
                if pixels[j] != 0:
                    pixels[j] -= 1
                else:
                    pixels[j] += 1
        if (i == lendata - 1):
            if (pixels[-1] % 2 == 0):
                if pixels[-1] != 0:
                    pixels[-1] -= 1
                else:
                    pixels[-1] += 1
        else:
            if (pixels[-1] % 2 != 0):
                pixels[-1] -= 1
        pixels = tuple(pixels)
        yield pixels[0:3]
        yield pixels[3:6]
        yield pixels[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(image_path, text, output_path):
    image = Image.open(image_path).convert('RGB')
    if (len(text) == 0):
        raise ValueError('Data is empty')
    newimg = image.copy()
    encode_enc(newimg, text)
    newimg.save(output_path, "PNG")

def decode(image_path):
    image = Image.open(image_path).convert('RGB')
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>StegoSafe | Open Innovation</title>
    <style>
        body { background-color: #0d0d0d; color: #00ff41; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        h1 { border-bottom: 2px solid #00ff41; padding-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }
        .container { display: flex; flex-wrap: wrap; gap: 50px; margin-top: 20px; justify-content: center; }
        .box { border: 1px solid #00ff41; padding: 30px; width: 300px; background: #111; box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); }
        input, button { width: 100%; margin-top: 15px; padding: 12px; background: #000; color: #fff; border: 1px solid #333; box-sizing: border-box; }
        button { background: #00ff41; color: #000; font-weight: bold; cursor: pointer; border: none; transition: 0.3s; }
        button:hover { background: #00cc33; box-shadow: 0 0 10px #00ff41; }
        .note { font-size: 10px; color: #666; margin-top: 5px; }
        .result { margin-top: 20px; padding: 10px; border: 1px dashed #00ff41; word-wrap: break-word; }
    </style>
</head>
<body>
    <h1>STEGO_SAFE // VIBEHACKS 2.0</h1>
    <div class="container">
        <div class="box">
            <h2>&gt; ENCRYPT DATA</h2>
            <form action="/encrypt" method="post" enctype="multipart/form-data">
                <label>1. Upload Carrier Image</label>
                <input type="file" name="file" required>
                <label>2. Secret Message</label>
                <input type="text" name="secret_text" placeholder="Confidential data..." required>
                <button type="submit">INJECT DATA</button>
            </form>
            <p class="note">Output will be a .PNG file.</p>
        </div>

        <div class="box">
            <h2>&gt; DECRYPT DATA</h2>
            <form action="/decrypt" method="post" enctype="multipart/form-data">
                <label>1. Upload Modified Image</label>
                <input type="file" name="file" required>
                <button type="submit">EXTRACT DATA</button>
            </form>
            {% if message %}
            <div class="result">
                <strong>DECODED:</strong><br>
                {{ message }}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    print("DEBUG: Encrypt route hit!")
    if 'file' not in request.files: return "No file", 400
    file = request.files['file']
    text = request.form.get('secret_text', '')
    
    if file.filename == '': return "No selected file", 400
    
    filepath = os.path.join(UPLOAD_FOLDER, "temp_upload.png")
    file.save(filepath)
    
    output_path = os.path.join(UPLOAD_FOLDER, "secret_output.png")
    try:
        encode(filepath, text, output_path)
        return send_file(output_path, as_attachment=True, download_name="stego_secret.png")
    except Exception as e:
        return f"Error: {e}"

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    print("DEBUG: Decrypt route hit!")
    if 'file' not in request.files: return "No file", 400
    file = request.files['file']
    if file.filename == '': return "No selected file", 400
    
    filepath = os.path.join(UPLOAD_FOLDER, "temp_decode.png")
    file.save(filepath)
    
    try:
        secret = decode(filepath)
        return render_template_string(HTML_TEMPLATE, message=secret)
    except Exception as e:
        return f"Error decoding: {e}"

if __name__ == '__main__':
    print("Server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)