import csv
import json

from django.shortcuts import get_object_or_404
from kanji.models import Radical, Kanji


def run():
    dic_by_sound ={}
    kanji = Kanji.objects.all().order_by('-radical__radical_number')
    # for k in kanji:
    #     onyomi = k.onyomi.split("、")
    #     for o in onyomi:
    #         if o not in dic_by_sound:
    #             if k.radical:
    #                 dic_by_sound[o] = [[k.radical.radical, k.kanji]]
    #             else:
    #                 dic_by_sound[o] = [['', k.kanji]]
    #         else:
    #             if k.radical:
    #                 dic_by_sound[o].append([k.radical.radical, k.kanji])
    #             else:
    #                 dic_by_sound[o].append(['', k.kanji])
    for k in kanji:
        onyomi = k.onyomi.split("、")
        for o in onyomi:
            if o not in dic_by_sound:
                if k.radical:
                    dic_by_sound[o] = {
                        'radical':[k.radical.radical],
                        'kanji':[k.kanji]
                    }
                else:
                    dic_by_sound[o] = {
                        'radical':[],
                        'kanji':[k.kanji]
                    }
            else:
                if k.radical:
                    if k.radical.radical not in dic_by_sound[o]['radical']:
                        dic_by_sound[o]['radical'].append(k.radical.radical)
                if k.kanji not in dic_by_sound[o]['kanji']:
                    dic_by_sound[o]['kanji'].append(k.kanji)
                
    # print(dic_by_sound)
    print(len(dic_by_sound))
    list_dic_by_sound = [dic_by_sound]
    
    # json_object = json.dumps(list_dic_by_sound, indent=4, ensure_ascii=False)
    # # json_object_2 = json.dumps(radical_dic, indent=4, ensure_ascii=False)

    # # Writing to sample.json
    # with open("scripts/kanji_by_sound_list.json", "w") as outfile:
    #     outfile.write(json_object)
    
