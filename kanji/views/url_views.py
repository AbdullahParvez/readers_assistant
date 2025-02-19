from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import logging
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView


import json


from ..models import Kanji, Radical
from ..services import get_kanji_info


class KanjiListView(ListView):
    model = Kanji
    context_object_name = "kanji_list"
    queryset = Kanji.objects.all().prefetch_related('radical').order_by('no_of_strokes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['word']=self.request.GET.get('word', '')
        context["radicals"] = Radical.objects.all().order_by('number_of_stroke')
        return context


def kanji_list_by_jlpt(request, level):
    kanji_list = Kanji.objects.filter(jlpt_level=level).order_by('no_of_strokes')
    radicals = Radical.objects.all().order_by('number_of_stroke')
    context = {
        'kanji_list':kanji_list,
        'radicals':radicals
    }
    return render(request, 'kanji/kanji_list.html', context)

def kanji_list_by_radical(request, radical_id):
    kanji_list = Kanji.objects.filter(radical__id=radical_id).order_by('no_of_strokes')
    radicals = Radical.objects.all().order_by('number_of_stroke')
    context = {
        'kanji_list':kanji_list,
        'radicals':radicals
    }
    return render(request, 'kanji/kanji_list.html', context)


class KanjiDetailView(DetailView):
    queryset = Kanji.objects.all()

    def get_object(self):
        obj = super().get_object()
        obj.save()
        return obj


class KanjiUpdateView(UpdateView):
    model=Kanji
    fields = ['kanji' ,'onyomi', 'kunyomi', 'radical', 'parts']
    template_name_suffixm = "_update_form"

    success_url ="/kanji/list/"


def kanji_search_view(request):
    word=request.GET.get('word', '')
    context = {
        'word':word,
    }
    return render(request, 'kanji/kanji_search.html', context)

def search_kanji(request):
    if request.method == "POST":
        data = json.load(request)
        # kanji = request.POST['data']
        kanji = data.get('kanji')
        context, success = get_kanji_info(kanji)
        return JsonResponse({"success": success, 'context': context},status=200)
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
                'k_jlpt': k.jlpt_level,
                'r_radical': k.radical.radical if k.radical else '',
                'r_meaning': k.radical.meaning if k.radical else '',
                'r_readings': k.radical.readings if k.radical else '',
            }
            return JsonResponse({"success": True, 'context': context},status=200)
        except ObjectDoesNotExist as err:
            # print(err)
            return JsonResponse({"success": False}, status=200)
