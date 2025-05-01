import os
from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import io

app = Flask(__name__)

# Thư mục lưu trữ ảnh đã chỉnh sửa
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lịch sử các thao tác chỉnh sửa ảnh
actions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file:
        img = Image.open(file.stream)
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        img.save(img_path)
        actions.append(('upload', img_path))
        return render_template('index.html', image_url=img_path)

@app.route('/perform_action', methods=['POST'])
def perform_action():
    action = request.form['action']
    current_image_path = actions[-1][1]
    img = Image.open(current_image_path)
    
    if action == 'bw':
        img = img.convert('L')
    elif action == 'blur':
        img = img.filter(ImageFilter.GaussianBlur(5))
    elif action == 'flip_h':
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif action == 'flip_v':
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    elif action == 'vintage':
        img = ImageOps.colorize(img.convert('L'), '#704214', '#c0c0c0')
    elif action == 'cool':
        img = ImageEnhance.Color(img).enhance(0.5)
    elif action == 'warm':
        img = ImageEnhance.Color(img).enhance(1.5)
    elif action == 'brighten':
        img = ImageEnhance.Brightness(img).enhance(1.5)
    elif action == 'contrast':
        img = ImageEnhance.Contrast(img).enhance(1.5)
    elif action == 'sharpen':
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    elif action == 'rotate':
        img = img.rotate(90, expand=True)
    elif action == 'crop':
        img = img.crop((100, 100, 400, 400))
    elif action == 'split_rgb':
        channel = request.form['channel']
        r, g, b = img.split()
        
        # Tạo ảnh mới cho mỗi kênh
        if channel == 'R':
            img = Image.merge('RGB', (r, Image.new('L', r.size, 0), Image.new('L', r.size, 0)))
        elif channel == 'G':
            img = Image.merge('RGB', (Image.new('L', g.size, 0), g, Image.new('L', g.size, 0)))
        elif channel == 'B':
            img = Image.merge('RGB', (Image.new('L', b.size, 0), Image.new('L', b.size, 0), b))
    
    # Lưu ảnh chỉnh sửa
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'edited_' + str(len(actions)) + '.png')
    img.save(img_path)
    actions.append((action, img_path))

    return render_template('index.html', image_url=img_path)

@app.route('/undo', methods=['POST'])
def undo_action():
    if len(actions) > 1:
        actions.pop()  # Xóa thao tác cuối cùng
        last_action = actions[-1]
        img_path = last_action[1]
        return render_template('index.html', image_url=img_path)
    else:
        return "No previous action"

@app.route('/download')
def download_image():
    last_action = actions[-1]
    return send_from_directory(app.config['UPLOAD_FOLDER'], os.path.basename(last_action[1]), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)