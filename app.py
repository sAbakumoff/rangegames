from flask import Flask, request, jsonify
from poker import Range, Combo, Hand
import random
import json
import pbots_calc

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

@app.route('/hand-vs-hand', methods=['POST'])
def test():
     h1 = request.form.get('h1')
     h2 = request.form.get('h2')
     return json.dumps(evalhtoh(h1, h2))

# def test(rangeTxt, handTxt):
#      rangeObj = Range(rangeTxt)
#      for h in rangeObj.hands:
#         calcInput = handTxt + ':' + str(h)
#         r = pbots_calc.calc(calcInput, "", "", 1000000)
#         if r:
#             print r.ev
#             #print zip(r.hands, r.ev)

def evalhtoh(h1, h2):
        calcInput = h1 + ':' + h2
        r = pbots_calc.calc(calcInput, "", "", 1000000)
        return r.ev

if __name__ == '__main__':
    app.run(debug=True)
