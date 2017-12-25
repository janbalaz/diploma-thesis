"""Routes frontend demands.
@author: Jan Balaz
"""

import os
from backend.model import Model
from backend.jsonencoder import JSONEncoder
from flask import Flask, request, abort

app = Flask(__name__)
MODEL = Model()


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
    return JSONEncoder().encode({})


@app.route("/categories/", methods=["GET"])
def categories():
    if request.method == "GET":
        categories = MODEL.get_all_categories()
        return JSONEncoder().encode(categories)
    else:
        abort(404)


@app.route("/classify/", methods=["POST"])
def classification_post():
    if request.method == "POST":
        text = request.data["text"]
        if text:
            success, message = MODEL.classify(text)
            if success:
                result = {"status": True, "result": message}
            else:
                result = {"status": False, "error": message} 
            return JSONEncoder().encode(result)       
        else:
            abort(400)
    else:
        abort(404)


@app.route("/classification/", methods=["GET"])
def classification_get():
    if request.method == "GET":
        post_id = request.args.get("post_id")
        if post_id:
            text = MODEL.get_classified_text(post_id)
            if text:
                result = {"status": True, "result": text}
            else:
                result = {"status": False, "error": text}
        else:
            classification = MODEL.get_all_classified()
            result = {"status": True, "result": classification}
    else:
        abort(404)
    return JSONEncoder().encode(result)


@app.teardown_appcontext
def close_database(exception):
    MODEL.close_connection()
    

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
