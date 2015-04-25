"""TODO desc
@author: Jan Balaz
"""


from backend.model import Model
from flask import Flask, request, session, url_for, redirect, abort, g, _app_ctx_stack
app = Flask(__name__)

MODEL = Model()

@app.route("/")
def main():
    return "Hello World!"

@app.route("/categories/", methods=["GET"])
def categories():
    if request.method == "GET":
        pass
    else:
        abort(404)

@app.route("/classification/<int:post_id>", methods=["GET","POST"])
def classification(post_id):
    if request.method == "POST":
        if request.form['text']:
            result = MODEL.classify(request.form['text'])
        else:
            error = "Text for classification not given."
    elif request.method == "GET":
        if post_id:
            pass    #TODO
        else:
            error = "Cannot return classification without id."
    else:
        abort(404)
    return error

@app.teardown_appcontext
def close_database(exception):
    pass

if __name__ == "__main__":
    app.run(debug=True)