import json
# Dictionary_Entry.drop_collection()
from kanji.models import Kanji

def run():
    file = open('scripts/final_kanji_parts.json', encoding="utf-8")
    data = json.load(file)
    kanji_dic = data[0]

    for key, val in kanji_dic.items():
        parts = ''
        for v in val:
            if parts:
                parts = parts+', '+v
            else:
                parts = parts+v

        if parts !='':
            Kanji.objects.filter(kanji=key).update(parts=parts)
