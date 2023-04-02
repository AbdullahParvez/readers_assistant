from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import logging

import json


from .models import Kanji, Radical


def search_kanji(request):
    if request.method == "POST" and request.is_ajax:
        data = json.load(request)
        # kanji = request.POST['data']
        kanji = data.get('kanji')
        k = get_object_or_404(Kanji, kanji=kanji)
        # print(k.kanji, k.onyomi, k.kunyomi, k.meaning, k.examples, k.no_of_strokes, k.radical)

        same_radical = Kanji.objects.filter(radical=k.radical).defer('kanji').order_by('jlpt_level')
        kanji_list = []
        for r in same_radical:
            kanji_list.append(r.kanji)
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
            'kanji_by_radical': kanji_list
        }

        # return JsonResponse({"success": True}, status=200)
        return JsonResponse({"success": True, 'context': context},status=200)
    return JsonResponse({"success": False}, status=400)


def kanji_hover(request):
    if request.method == "POST":
        data = json.load(request)
        kanji = data.get('kanji')
        k = get_object_or_404(Kanji, kanji=kanji)
        context = {
            'kanji': k.kanji,
            'k_onyomi': k.onyomi,
            'k_kunyomi':k.kunyomi,
            'k_meaning':k.meaning,
        }
        return JsonResponse({"success": True, 'context': context},status=200)
    return JsonResponse({"success": False}, status=400)
