import json
# Dictionary_Entry.drop_collection()
from kanji.models import Kanji, Radical
from jmdict.models import Dictionary_Entry, Sense, Example
from sudachipy import tokenizer
from sudachipy import dictionary
from mongoengine import *
from mongoengine.queryset.visitor import Q

connect('jmdict')
tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
mode = tokenizer.Tokenizer.SplitMode.C

def run():
    file = open('scripts/kanjvg_kanji_parts.json', encoding="utf-8")
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
