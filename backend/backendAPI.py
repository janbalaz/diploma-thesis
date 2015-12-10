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


@app.route("/<int:type>")
def main(type):
    if type == 1:
        data = {"dataArray" : [
             ["Element", "Density", {"role": "style"}],
             ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ],
            ["Copper", 8.94, "#b87333"],
             ["Silver", 10.49, "silver"],
             ["Gold", 19.30, "gold"],
             ["Platinum", 21.45, "color: #e5e4e2" ]
          ],
          "options": {
            "title": "Density of Precious Metals, in g/cm^3",
            "bar": {"groupWidth": "95%"},
            "legend": {"position": "none"}
          }}
    elif type == 2:
        data = {"dataArray" : [
            ['Task', 'Hours per Day'],
            ['Work',     11],
            ['Eat',      2],
            ['Commute',  2],
            ['Watch TV', 2],
            ['Sleep',    7]
          ],
          "options": {
            "title": "Density of Precious Metals, in g/cm^3",
            "bar": {"groupWidth": "95%"},
            "legend": {"position": "none"},
              "pieHole": 0.4
          }}
    else:
        data = {"dataArray" : [
          ['Location', 'Parent', 'Market trade volume (size)', 'Market increase/decrease (color)'],
          ['Global',    None,                 0,                               0],
          ['America',   'Global',             0,                               0],
          ['Europe',    'Global',             0,                               0],
          ['Asia',      'Global',             0,                               0],
          ['Australia', 'Global',             0,                               0],
          ['Africa',    'Global',             0,                               0],
          ['Brazil',    'America',            11,                              10],
          ['USA',       'America',            52,                              31],
          ['Mexico',    'America',            24,                              12],
          ['Canada',    'America',            16,                              -23],
          ['France',    'Europe',             42,                              -11],
          ['Germany',   'Europe',             31,                              -2],
          ['Sweden',    'Europe',             22,                              -13],
          ['Italy',     'Europe',             17,                              4],
          ['UK',        'Europe',             21,                              -5],
          ['China',     'Asia',               36,                              4],
          ['Japan',     'Asia',               20,                              -12],
          ['India',     'Asia',               40,                              63],
          ['Laos',      'Asia',               4,                               34],
          ['Mongolia',  'Asia',               1,                               -5],
          ['Israel',    'Asia',               12,                              24],
          ['Iran',      'Asia',               18,                              13],
          ['Pakistan',  'Asia',               11,                              -52],
          ['Egypt',     'Africa',             21,                              0],
          ['S. Africa', 'Africa',             30,                              43],
          ['Sudan',     'Africa',             12,                              2],
          ['Congo',     'Africa',             10,                              12],
          ['Zaire',     'Africa',             8,                               10]
        ],
          "options": {
            "title": "Density of Precious Metals, in g/cm^3",
            "bar": {"groupWidth": "95%"},
            "legend": {"position": "none"},
              "pieHole": 0.4
          }}
    return JSONEncoder().encode(data)


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