from rest_framework.generics import GenericAPIView
from ..serializers import KanjiSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Kanji

def get_kanji_details(kanji):
    '''retrieve and rearrange meaning of a word'''
    k = get_object_or_404(Kanji, kanji=kanji)

    # same_radical = Kanji.objects.filter(radical=k.radical).defer('kanji').order_by('jlpt_level')
    # kanji_list = []
    # for r in same_radical:
    #     kanji_list.append(r.kanji)

    similar_kanji = Kanji.objects.filter(parts__contains=k.kanji)
    
    similar_kanji_list = []
    for s in similar_kanji:
        if s.kanji != k.kanji:
            similar_kanji_list.append(s.kanji)
    # print(similar_kanji_list)
    context = {
        'kanji': k.kanji,
        'k_onyomi': k.onyomi,
        'k_kunyomi':k.kunyomi,
        'k_meaning':k.meaning,
        # 'k_examples': k.examples,
        'k_jlpt': k.jlpt_level,
        'radical': k.radical.radical,
        'r_meaning': k.radical.meaning,
        'r_readings': k.radical.readings,
        # 'r_alternatives': k.radical.alternative,
        # 'kanji_by_radical': kanji_list,
        'similar_sounded_kanji':similar_kanji_list
    }
    return context


class GetKanjiDetails(GenericAPIView):
    """
    Return vocab details.
    """
    serializer_class = KanjiSerializer

    def get(self, request, kanji, format=None):
        # vocab = self.kwargs['vocab']
        context = get_kanji_details(kanji=kanji)
        
        serializer = self.get_serializer(data={'details':str(context)})
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
