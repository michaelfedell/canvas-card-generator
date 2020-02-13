"""[summary]."""
import random

from flask import Flask, render_template, make_response
from flask import redirect, request, jsonify, url_for

from canvas import STYLES, styles, randomize_colors, update_canvas_id

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    response = jsonify({
        'status': 'great job, you found the index'
    })
    return make_response(response, 200)


@app.route('/canvas', methods=['GET'])
def get_randomized_canvas():
    style = random.choice(STYLES)
    response = jsonify({
        'msg': 'A random style was chosen',
        'style': style,
        'original_code': styles[style]['code'],
        'randomized': randomize_colors(styles[style]['code'])
    })
    return make_response(response, 200)


@app.route('/canvas/og', methods=['GET'])
def get_random_canvas():
    style = random.choice(STYLES)
    response = jsonify({
        'msg': 'A random style was chosen',
        'style': style,
        'original_code': styles[style]['code']
    })
    return make_response(response, 200)


@app.route('/canvas/render', methods=['GET'])
def render_randomized_canvas():
    style = random.choice(STYLES)
    randomized = randomize_colors(styles[style]['code'])
    clean = update_canvas_id(randomized)
    return render_template(
        'layouts/canvas.html',
        title='Random Canvas',
        name=f'Randomized {style}'.title(),
        code=clean
    )


@app.route('/canvas/<style>', methods=['GET'])
def get_canvas(style: str):
    if style in STYLES:
        response = jsonify({
            'style': style,
            'original_code': styles[style]['code'],
            'randomized': randomize_colors(styles[style]['code'])
        })
        return make_response(response, 200)
    else:
        response = jsonify({
            'msg': f'Sorry, but {style} is not an available style'
        })
        return make_response(response, 400)
