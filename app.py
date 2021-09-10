import os
from PIL import Image, ImageStat, ImageColor
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def colorcheck(file, color):
    im = Image.open(file)
    im_width, im_height = im.size
    color_rgb = ImageColor.getrgb(color)
    count_w = 0
    count_b = 0
    count_color = 0
    for x in range(im_width):
        for y in range(im_height):
            px = im.load()[x, y]
            if px == (0, 0, 0):
                count_b += 1
            elif px == (255, 255, 255):
                count_w += 1
            if px == color_rgb:
                count_color += 1
    return count_b, count_w, count_color


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    count_b = request.args.get('count_b', '')
    count_w = request.args.get('count_w', '')
    count_color = request.args.get('count_color', '')
    color = request.args.get('color', '')
    if request.method == 'POST':
        file = request.files['file']
        color = request.values['color']
        count_b, count_w, count_color = colorcheck(file, color)
        # return redirect(url_for('upload_file',
        #                         count_b=count_b, count_w=count_w, count_color=count_color, color=color))
    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <body>
        <h1>Анализ пикселей</h1>
        <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <p> Введите код цвета <input type="text" name="color"></p>
            <p><input type=submit value=Upload></p>
        </form>
        <h2>Черных пикселей: {count_b}</h2>   
        <h2>Белых пикселей: {count_w}</h2>
        <h2>Пикселей цвета {color}: {count_color}</h2>
    </body     
    '''


@app.route('/new/')
def uploaded_file():
    filename = request.args.get('filename', 'Clear')
    return f'''
        <!doctype html>
        <title>Upload new File</title>
   
        <p>
        {filename}
        </p>
 
        '''


if __name__ == '__main__':
    app.run()
