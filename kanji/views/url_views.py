from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import logging
from django.core.exceptions import ObjectDoesNotExist

import json


from ..models import Kanji, Radical

def search_word(request):
    return render(request, "kanji/search_word.html")


def search_kanji(request):
    if request.method == "POST":
        data = json.load(request)
        # kanji = request.POST['data']
        kanji = data.get('kanji')
        k = get_object_or_404(Kanji, kanji=kanji)
        # print(k.kanji, k.onyomi, k.kunyomi, k.meaning, k.examples, k.no_of_strokes, k.radical)

        same_radical = Kanji.objects.filter(radical=k.radical).defer('kanji').order_by('jlpt_level')
        kanji_list = []
        for r in same_radical:
            kanji_list.append(r.kanji)

        similar_kanji = Kanji.objects.filter(parts__contains=k.kanji)
        
        similar_sounded_kanji = []
        for s in similar_kanji:
            if s.kanji != k.kanji:
                similar_sounded_kanji.append(s.kanji)
        print(similar_sounded_kanji)
        context = {
            'kanji': k.kanji,
            'k_onyomi': k.onyomi,
            'k_kunyomi':k.kunyomi,
            'k_meaning':k.meaning,
            'k_examples': k.examples,
            'k_jlpt': k.jlpt_level,
            'radical': k.radical.radical,
            'r_meaning': k.radical.meaning,
            'r_readings': k.radical.readings,
            'r_alternatives': k.radical.alternative,
            'kanji_by_radical': kanji_list,
            'similar_sounded_kanji':similar_sounded_kanji
        }

        # return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": True, 'context': context},status=200)
    return JsonResponse({"success": False}, status=400)


def kanji_hover(request):
    if request.method == "POST":
        data = json.load(request)
        kanji = data.get('kanji')
        try:
            k = Kanji.objects.get(kanji=kanji)
            context = {
                'kanji': k.kanji,
                'k_onyomi': k.onyomi,
                'k_kunyomi':k.kunyomi,
                'k_meaning':k.meaning,
                'k_jlpt': k.jlpt_level
            }
            return JsonResponse({"success": True, 'context': context},status=200)
        except ObjectDoesNotExist as err:
            print(err)
            return JsonResponse({"success": False}, status=200)
