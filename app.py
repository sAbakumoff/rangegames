from flask import Flask, request, jsonify
from poker import Range, Combo, Hand
import random
import json
import pbots_calc
import itertools
import csv

from encoder import *

app = Flask(__name__)

d = dict()

with open('ranges.txt') as f:
    ranges = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
ranges = [x.strip() for x in ranges] 

@app.route("/")
def serve_index():
    return app.send_static_file("hand-vs-range.html")

@app.route("/range")
def serve_range():
    rgText = random.choice(ranges)
    rgObj = RangeWrapper(rgText)
    return json.dumps(rgObj, cls=MyEncoder)

@app.route("/range_html", methods=['POST'])
def buildRange():
    rgObj = RangeWrapper(request.form.get('range'))
    return json.dumps(rgObj, cls=MyEncoder)

@app.route("/hand")
def serve_hand():
    return str(Hand.make_random())

@app.route('/hand-vs-hand', methods=['POST'])
def test():
     h1 = request.form.get('h1')
     h2 = request.form.get('h2')
     return json.dumps(evalhtoh(h1, h2))

@app.route('/evaluate', methods=['POST'])
def evaluate_worker():
     r1 = request.form.get('r1')
     r2 = request.form.get('r2')
     board = request.form.get('board')
     res = pbots_calc.calc(r1 + ":" + r2, board, "", 1000000)
     return json.dumps(res.ev)


# def test(rangeTxt, handTxt):
#      rangeObj = Range(rangeTxt)
#      for h in rangeObj.hands:
#         calcInput = handTxt + ':' + str(h)
#         r = pbots_calc.calc(calcInput, "", "", 1000000)
#         if r:
#             print r.ev
#             #print zip(r.hands, r.ev)

def evalhtoh(h1, h2):
        if h1 == h2 :
            return [0.5, 0.5]
        h_key = h1 + ':' + h2
        if d.has_key(h_key) :
            ev =  d[h_key]
            return [ev, 1-ev]
        else:
            h_key = h2 + ':' + h1
            ev =  1 - d[h_key]
            return [ev, 1-ev]
        

def fill_hu_cache():
    with open('hu.csv', 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for c in list(itertools.combinations(list(Hand), 2)):
            ci = str(c[0]) + ':' + str(c[1])
            r = pbots_calc.calc(ci, "", "", 1000000)
            wr.writerow([ci, r.ev[0]])

def read_hu_cache():
    with open('hu.csv', 'rb') as csvfile:
        r = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in r:
            d[row[0]] = float(row[1])


if __name__ == '__main__':
    read_hu_cache()
    app.run(debug=True)
    #fill_hu_cache()
