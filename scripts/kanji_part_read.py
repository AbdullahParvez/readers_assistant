from kanji.models import Kanji

import json
# Dictionary_Entry.drop_collection()
from kanji.models import Kanji



def run():
    file = open('scripts/kanji_parts.json', encoding="utf-8")
    data = json.load(file)
    kanji_dic = data[0]

    file = open('scripts/kanji_part_list.json', encoding="utf-8")
    data = json.load(file)
    kanji_dic2 = data[0]

    for key, val in kanji_dic.items():
        if key not in kanji_dic2:
            # print(key)
            kanji_dic2[key] = val

    kanji_dict = [kanji_dic2]

    json_object = json.dumps(kanji_dict, indent=4, ensure_ascii=False)
    # json_object_2 = json.dumps(radical_dic, indent=4, ensure_ascii=False)

    # Writing to sample.json
    with open("scripts/final_kanji_parts.json", "w") as outfile:
        outfile.write(json_object)
