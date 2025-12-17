StegoSafe: Invisible Digital Watermarking

### 🚀 Project Overview
StegoSafe is an Open Innovation project built for **VIbehacks 2.0**. It addresses the issue of digital art theft by embedding invisible, encrypted copyright data directly into image pixels using **LSB (Least Significant Bit) Steganography**.

Unlike traditional metadata (which can be stripped), StegoSafe modifies the actual binary data of the image, making the watermark an intrinsic part of the file.

### 🛠️ Tech Stack
- **Backend:** Python 3.14
- **Algorithm:** Custom LSB Bitwise Manipulation
- **Framework:** Flask (Server-side rendering)
- **Image Processing:** Pillow (PIL)

### ⚙️ How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/StegoSafe-OpenInnovation.git](https://github.com/your-username/StegoSafe-OpenInnovation.git)
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python3 main.py
Open http://127.0.0.1:5000 in your browser.

🔮 Future Scope

AES-256 Encryption for the hidden text.

Support for Audio Steganography (.wav files).

Blockchain integration for immutable ownership proof.


**Final Push:**
After saving the README:
```bash
git add README.md
git commit -m "Add documentation"
git push
