from flask import Flask, render_template, request, jsonify
from PIL import Image
import io

app = Flask(__name__)

def image_to_palette_all(image_bytes, max_palette_size=256):
    """
    Convert image to a paletted image (adaptive) and return all palette colors
    ordered by frequency (most used first). max_palette_size caps the number
    of colors chosen by adaptive quantization (default 256).
    """
    img = Image.open(io.BytesIO(image_bytes)).convert('RGBA')
    # Resize to speed up processing while keeping representative colors
    img.thumbnail((800, 800))
    # Paste onto white background to handle alpha
    bg = Image.new('RGB', img.size, (255, 255, 255))
    alpha = img.split()[3] if img.mode == 'RGBA' else None
    bg.paste(img, mask=alpha)

    # Convert to paletted image using an adaptive palette with up to max_palette_size colors
    paletted = bg.convert('P', palette=Image.ADAPTIVE, colors=max_palette_size)

    # getcolors needs a max; supply the pixel count to ensure it returns counts
    maxcount = bg.size[0] * bg.size[1] + 1
    color_counts = paletted.getcolors(maxcount)
    if not color_counts:
        # fallback — quantize explicitly and re-run
        paletted = bg.quantize(colors=max_palette_size, method=Image.MEDIANCUT)
        color_counts = paletted.getcolors(maxcount) or []

    palette = paletted.getpalette()  # flat list [r,g,b, r,g,b, ...]
    # color_counts is list of (count, palette_index)
    # sort by count descending (getcolors already generally returns counts but sort to be safe)
    color_counts.sort(reverse=True, key=lambda x: x[0])

    seen_hex = []
    hex_colors = []
    for count, idx in color_counts:
        base = idx * 3
        if base + 2 >= len(palette):
            continue
        r = palette[base]
        g = palette[base + 1]
        b = palette[base + 2]
        h = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        if h not in seen_hex:
            seen_hex.append(h)
            hex_colors.append(h)

    # hex_colors now contains up to max_palette_size colors ordered by frequency.
    return hex_colors

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    f = request.files['image']
    try:
        img_bytes = f.read()
        # Extract up to 256 representative colors (you can change this limit)
        colors = image_to_palette_all(img_bytes, max_palette_size=256)
    except Exception as e:
        return jsonify({'error': 'Server error: ' + str(e)}), 500

    return jsonify({'colors': colors})

if __name__ == '__main__':
    app.run(debug=True)
