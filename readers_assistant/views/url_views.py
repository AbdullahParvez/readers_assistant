'''view for common function'''

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from sudachipy import tokenizer
from sudachipy import dictionary

from jmdict.models import Dictionary_Entry, Sense, Example

from mongoengine import *
from mongoengine.queryset.visitor import Q
import re

connect('jmdict')
tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
mode = tokenizer.Tokenizer.SplitMode.C

def get_word_meaning(request):
    if request.method == "POST":
        context = {}
        # import time
        # start = time.time()
        data = json.load(request)
        selected_text = data['word'].replace(" ", "")
        result = Dictionary_Entry.objects(Q(k_ele__exact=selected_text)|Q(r_ele__exact=selected_text))
        root_word = selected_text
        if not result:
            tokenize_words = tokenizer_obj.tokenize(selected_text, mode)
            token_word = tokenize_words[0]
            for token in tokenize_words:
                if len(str(token))>len(str(token_word)):
                    token_word=token
            word = token_word.dictionary_form()
            result = Dictionary_Entry.objects(Q(k_ele__exact=word)|Q(r_ele__exact=word))
            if not result:
                normalized_word = token_word.normalized_form()
                result = Dictionary_Entry.objects(Q(k_ele__exact=normalized_word)|Q(r_ele__exact=normalized_word))
            root_word = str(token_word)
        meaning = get_meaning(result)
        kanji_regex = re.compile("[\u4e00-\u9faf]+")

        # find all the matches in the text
        kanji_matches=[]
        try:
            kanji_matches = list(kanji_regex.findall(root_word)[0])
        except Exception:
            pass
        context['meanings'] = meaning
        context['root_word'] = root_word
        context['kanjis'] = kanji_matches
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
