from PIL import Image, ImageColor, UnidentifiedImageError
from flask import Flask, request, render_template
import logging
from pythonjsonlogger import jsonlogger

app = Flask(__name__)
logger = logging.getLogger()
logHandler = logging.FileHandler('info.log')
formatter = jsonlogger.JsonFormatter('%(asctime)%(message)')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)


def color_check(file, color):
    im = Image.open(file)
    picture = im.load()
    im_width, im_height = im.size
    color_rgb = ImageColor.getrgb(color)
    count_w = 0
    count_b = 0
    count_color = 0
    for x in range(im_width):
        for y in range(im_height):
            px = picture[x, y]
            if px == (0, 0, 0):
                count_b += 1
            elif px == (255, 255, 255):
                count_w += 1
            if px == color_rgb:
                count_color += 1
    return count_b, count_w, count_color


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    count_wb = ''
    count_color = ''
    color = ''
    error = ''
    if request.method == 'POST':
        file = request.files['file']
        color = request.values['color']
        try:
            count_b, count_w, count_color = color_check(file, color)
            if count_b > count_w:
                count_wb = 'Черных пикселей больше чем белых'
            else:
                count_wb = 'Белых пикселей больше чем черных'
        except ValueError:
            error = 'Недопустимый код цвета'
            color = ''
        except UnidentifiedImageError:
            error = 'Недопустимый тип файла'
        logger.info(f'file: {file.filename}, count_wb: {count_wb}, color: {color}, count_color: {count_color}, error: {error}')
    return render_template("index.html", error=error, count_wb=count_wb, color=color, count_color=count_color)


if __name__ == '__main__':
    app.run()
