'''This file is created by amp to get all the kanji part. It is not a part of the library'''
import csv
import json
# from kvg_lookup import characterSummary, strokeGroupSummary
from utils import listSvgFiles, canonicalId
from kanjivg import Stroke, StrokeGr


def unicode(s):
    return s
def unichr(c):
    return chr(c)
	
def strokeGroupSummary(gr, indent = 0):
    if not isinstance(gr, StrokeGr):
        raise Exception("Invalid structure")
    parts = []
    print(gr)
    if gr.element is not None and len(gr.element) > 0:
        parts.append(gr.element)

    for g in gr.childs:
        if isinstance(g, StrokeGr):
            parts.extend(strokeGroupSummary(g, indent + 1))
    return parts


kan = open('../kanji.csv')

reader_kan = csv.reader(kan)
next(reader_kan, None)
# kanji_part_list = []
kanji_dict = {}
for row in reader_kan:
    # print(row)

    kan = row[1]
    # print(kan)
    
    id = canonicalId(kan)
    try:
        kanji = [(f.path, f.read()) for f in listSvgFiles("./kanji/") if f.id == id]
        kanji_parts = []
        for i, (path, c) in enumerate(kanji):
            parts = strokeGroupSummary(c.strokes)
            for part in parts:
                if part not in kanji_parts:
                    kanji_parts.append(part)
                    # print(kanji_parts)
        # print(kan, kanji_parts)
        kanji_dict[kan]=kanji_parts
    except:
        continue

kanji_dict = [kanji_dict]

json_object = json.dumps(kanji_dict, indent=4, ensure_ascii=False)
# json_object_2 = json.dumps(radical_dic, indent=4, ensure_ascii=False)

# Writing to sample.json
with open("../kanji_part_list.json", "w") as outfile:
    outfile.write(json_object)
   
#     print(strokeGroupSummary(c.strokes)) 
# print(kvg_lookup.commandFindSvg('校'))
