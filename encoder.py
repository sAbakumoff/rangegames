from poker import Range, Combo, Hand
import random
import json

class RangeWrapper():
    def __init__(self, rangeStr=""):
        self.rangeStr = rangeStr
        self.range = Range(rangeStr)

class MyEncoder(json.JSONEncoder):
   def default(self, obj):
        if isinstance(obj, RangeWrapper): 
            combos = 0
            pairs = 0
            suited = 0
            offsuited = 0
            for combo in obj.range.combos :
                combos = combos + 1
                if combo.is_pair :
                    pairs = pairs + 1
                elif combo.is_suited :
                    suited = suited + 1
                elif combo.is_offsuit :
                    offsuited = offsuited + 1
            return { "rgText" : obj.rangeStr, "rgHtml" : obj.range.to_html(), "combos" : combos, "pairs" : pairs, "suited" : suited, "offsuited" : offsuited  }
        return json.JSONEncoder.default(self, obj)
