'''view for common function'''

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from sudachipy import tokenizer
from sudachipy import dictionary

from jmdict.models import Dictionary_Entry, Sense, Example

from mongoengine import *

connect('jmdict')
tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
mode = tokenizer.Tokenizer.SplitMode.A

def get_word_meaning(request):
    if request.method == "POST":
        context = {}
        data = json.load(request)
        # print(data['word'])
        result = Dictionary_Entry.objects(k_ele__exact=data['word'])
        meaning = None
        # print(result)
        if result:
            # print(result)
            # result = jam.lookup(data['word'])
            meaning = get_meaning(result)
        else:
            # print('No result tokenize start')
            m = tokenizer_obj.tokenize(data['word'], mode)[0]
            word = m.dictionary_form()
            if word:
                if '覚まし' in data['word'] and 'し'==data['word'][-1]:
                    word = data['word'].replace('覚まし','覚ます')
            result = Dictionary_Entry.objects(k_ele__exact=word)
            if result:
                meaning = get_meaning(result)
            else:
                # print('None')
                pass
        # context['constructions_with_budget'] = constructions_with_budget
        context['meanings'] = meaning
        return JsonResponse({"success": True, 'context': context}, status=200)

    return JsonResponse({"success": False}, status=400)

def get_meaning(result):
    meanings = []
    for res in result:
        meaning = {}
        meaning['k_ele'] = ', '.join(res.k_ele)
        meaning['r_ele'] = res.r_ele
        # print(res.k_ele)
        # print(res.r_ele)
                # print(res.sense.meaning)
                # print(res.sense.pos)
                # print(res.sense.example)
        m_sense=[]
        sense = res.sense
        for se in sense:
            temp = {}
            temp['meaning']=se.meaning
            temp['pos']=se.pos
            # print(se.meaning)
            # print(se.pos)
            m_sense.append(temp)
        meaning['sense'] = m_sense
        meanings.append(meaning)
    return meanings
