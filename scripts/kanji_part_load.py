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
    # with open('scripts/data.json') as file:
    file = open('scripts/kanjvg_kanji_parts.json')
    data = json.load(file)
    kanji_dic = data[0]

    for key, val in kanji_dic.items():
        parts = ''
        for v in val:
            if parts:
                parts = parts+', '+v
            else:
                parts = parts+v
        # print(parts)

        if parts !='':
            Kanji.objects.filter(kanji=key).update(parts=parts)

    # kanji = Kanji.objects.get(kanji='術')
    # parts = kanji.parts.split(', ')
    # for part in parts:
        
        
    #     qs = Kanji.objects.filter(parts__contains=part).values('kanji','onyomi')
    #     print(part)

    #     k_list = [q['kanji'] for q in qs]
    #     print(k_list)
    #     k_list = []
    #     try:
    #         # r_qs = Radical.objects.get(radical=part)
    #         # print(r_qs.readings)
    #         part_kanji = Kanji.objects.get(kanji=part)
    #         kun_list = part_kanji.onyomi.split(', ')
    #         print(kun_list)
    #         for kun in kun_list:
    #             for q in qs:
    #                 # print(q['onyomi'])
    #                 if kun in q['onyomi']:
    #                     print(q['onyomi'])
    #                     k_list.append(q['kanji'])
    #     except:
    #         print(part)

        
        # print(k_list)

    # kanjis = Kanji.objects.all()
    # kanji_dic = {}
    # for k in kanjis:
    #     part_contains_kanji = Kanji.objects.filter(parts__contains=k.kanji)
    #     parts = []
    #     for p in part_contains_kanji:
    #         parts.append(p.kanji)
    #     kanji_dic[k.kanji]=parts
    # meanings = []
    # selected_text = '本'
    # print(selected_text)
    # results = Dictionary_Entry.objects(Q(k_ele__exact=selected_text)|Q(r_ele__exact=selected_text))
    # count = 1
    # for res in results:
    #     meaning = {}
    #     meaning['no'] = count
    #     meaning['k_ele'] = ', '.join(res.k_ele)
    #     meaning['r_ele'] = res.r_ele
    #     # print(res.k_ele)
    #     # print(res.r_ele)
    #             # print(res.sense.meaning)
    #             # print(res.sense.pos)
    #             # print(res.sense.example)
    #     m_sense=[]
    #     sense = res.sense
    #     for se in sense:
    #         temp = {}
    #         temp['meaning']=se.meaning
    #         temp['pos']=se.pos
    #         # print(se.meaning)
    #         # print(se.pos)
    #         m_sense.append(temp)
    #         example = se.example
    #         examples = []
    #         for ex in example:
    #             tmp = {}
    #             if ex.ex_text == selected_text:
    #                 tmp['ex_sent_jpn'] = ex.ex_sent_jpn
    #                 tmp['ex_sent_eng'] = ex.ex_sent_eng
    #                 examples.append(tmp)
    #         temp['examples'] = examples
    #     meaning['sense'] = m_sense
    #     meanings.append(meaning)
    #     count +=1
    # print(meanings)
    