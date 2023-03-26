'''view for common function'''

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from sudachipy import tokenizer
from sudachipy import dictionary

from jmdict.models import Dictionary_Entry, Sense, Example

from mongoengine import *
from mongoengine.queryset.visitor import Q

connect('jmdict')
tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
mode = tokenizer.Tokenizer.SplitMode.C

def get_word_meaning(request):
    if request.method == "POST":
        context = {}
        # import time
        # start = time.time()
        data = json.load(request)
        selelected_text = data['word']
        result = Dictionary_Entry.objects(Q(k_ele__exact=selelected_text)|Q(r_ele__exact=selelected_text))
        root_word = selelected_text
        if not result:
            tokenize_words = tokenizer_obj.tokenize(data['word'], mode)[0]
            word = tokenize_words.dictionary_form()
            result = Dictionary_Entry.objects(Q(k_ele__exact=word)|Q(r_ele__exact=word))
            if not result:
                word = tokenize_words.normalized_form()
                result = Dictionary_Entry.objects(Q(k_ele__exact=selelected_text)|Q(r_ele__exact=selelected_text))
            root_word = str(tokenize_words)
        # print(root_word)
        meaning = get_meaning(result)
        context['meanings'] = meaning
        context['root_word'] = root_word
        return JsonResponse({"success": True, 'context': context}, status=200)

    return JsonResponse({"success": False}, status=400)

def get_meaning(result):
    meanings = []
    count = 1
    for res in result:
        meaning = {}
        meaning['no'] = count
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
        count +=1
    return meanings
