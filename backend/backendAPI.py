"""Routes frontend demands.
@author: Jan Balaz
"""

import os
from backend.model import Model
import json
from bson import json_util
from flask import Flask, request, abort
from classification.classifications import Algos

app = Flask(__name__)
MODEL_LDA = Model(Algos.LDA)
MODEL_LSI = Model(Algos.LSI)


def get_model(model):
    if model.lower() == "lda":
        return MODEL_LDA
    else:
        return MODEL_LSI


@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get('Access-Control-Request-Headers',
                                                                       'Authorization')
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp


@app.route("/")
def main():
    return app.send_static_file('frontend/dist/index.html')


@app.route("/categories/", methods=["GET"])
def categories():
    if request.method == "GET":
        model = request.args.get("model")
        if model:
            num_words = int(request.args.get("num_words")) if request.args.get("num_words") else 10
            categories = get_model(model).get_all_categories(num_words)
            return json.dumps(categories, default=json_util.default)
        else:
            abort(400)
    else:
        abort(404)


@app.route("/classify/", methods=["POST"])
def classification_post():
    if request.method == "POST":
        text = request.get_json()["text"]
        model = request.args.get("model")
        if text and model:
            success, message = get_model(model).classify(text)
            if success:
                payload = {
                    "id": message
                }
            else:
                payload = {
                    "error": str(message)
                }

            return json.dumps({
                "status": success,
                "payload": payload
            }, default=json_util.default)
        else:
            abort(400)
    else:
        abort(404)


@app.route("/classification/", methods=["GET"])
def classification_get():
    if request.method == "GET":
        model = request.args.get("model")
        if model:
            post_id = request.args.get("id")
            if post_id:
                entry = get_model(model).get_classified_text(post_id)
                if entry:
                    result = {"status": True, "payload": {
                        "entries": [entry]
                    }}
                else:
                    result = {"status": False, "payload": {
                        "error": "No results found."
                    }}
            else:
                entries = get_model(model).get_all_classified()
                if entries:
                    result = {"status": True, "payload": {
                        "entries": entries
                    }}
                else:
                    result = {"status": False, "payload": {
                        "error": "No results found."
                    }}

            return json.dumps(result, default=json_util.default)
        else:
            abort(400)
    else:
        abort(404)


@app.teardown_appcontext
def close_database(exception):
    try:
        MODEL_LDA.close_connection()
        MODEL_LSI.close_connection()
    except Exception:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
