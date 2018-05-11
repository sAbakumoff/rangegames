from flask import Flask, jsonify
from poker import Range, Combo, Hand
import random
import json
from encoder import *

app = Flask(__name__)

with open('ranges.txt') as f:
    ranges = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
ranges = [x.strip() for x in ranges] 

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

@app.route("/range")
def serve_range():
    rgText = random.choice(ranges)
    rgObj = RangeWrapper(rgText)
    return json.dumps(rgObj, cls=MyEncoder)

@app.route("/range0")
def serve_range0():
    return Range('XX').to_html()


if __name__ == '__main__':
    app.run(debug=True)
