from flask import Flask, jsonify
from poker import Range
import random

app = Flask(__name__)

ranges = []
ranges.append('JJ+, AK+')
ranges.append('77+, AQ+')
ranges.append('55+, ATo+, A8s+, A5s')


@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

@app.route("/range")
def serve_range():
    rgText = random.choice(ranges)
    rgObj = Range(rgText)
    return jsonify(
        rgText = rgText,
        rgHtml = rgObj.to_html(),
        percent = rgObj.percent
    )

@app.route("/range0")
def serve_range0():
    return Range('XX').to_html()


if __name__ == '__main__':
    app.run(debug=True)
