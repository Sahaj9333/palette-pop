Palette Pop — Color Palette Extractor

A single-purpose web tool that extracts all representative colors from any uploaded image.
Upload → Extract → Copy hex codes → Export CSS variables → Download JSON palette.

🚀Features
1.Upload any image (PNG/JPG/WebP)
2.Extract adaptive palette (up to 256 colors)
3.View clean color swatches
4.Copy any color (HEX)
5.Copy entire CSS variable set
6.Download JSON palette
7.Gradient + UI preview generated automatically

🛠 Tech Stack

1.Python + Flask
2.Pillow (PIL) for image quantization
3.HTML + CSS + JS
4.Bootstrap 5
5.Kiro for workflow acceleration

Install & Run

1️⃣ Clone repository
git clone https://github.com/<your-username>/palette-pop.git
cd palette-pop

2️⃣ Create virtual environment
python -m venv venv

Activate:

Windows:-
venv\Scripts\activate

Linux/Mac:-
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run Flask server
python app.py

Then open
📍 http://127.0.0.1:5000

📁 Project Structure
palette-pop/
│── app.py
│── requirements.txt
│── README.md
│── /kiro/kiro-config.json
│── /templates/index.html
