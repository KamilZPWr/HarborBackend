from flask import Flask, jsonify, request

from handler import handle_category_request
from src.backend import process

app = Flask(__name__)

TEXT = "text"
ROOMS_N_MIN = "rooms_n_min"
ROOMS_N_MAX = "rooms_n_max"
SIZE_MIN = "size_min"
SIZE_MAX = "size_max"
PRICE_MIN = "price_min"
PRICE_MAX = "price_max"


@app.route('/api')
def hello():
    keyword: str = request.args.get('keyword')
    handle_category_request(keyword)
    return jsonify(keyword)


@app.route('/real_estates', methods=['POST'])
def tmp():
    content = request.json

    real_estates = process(
        content[TEXT],
        content[PRICE_MAX],
        content[PRICE_MIN],
        content[SIZE_MAX],
        content[SIZE_MIN],
        content[ROOMS_N_MAX],
        content[ROOMS_N_MIN],
    )

    return jsonify(real_estates)
