from rest_framework.generics import GenericAPIView
from ..serializers import KanjiSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from ..models import Kanji, Radical
from ..services import get_kanji_info

def get_kanji_details(kanji):
    '''retrieve and rearrange meaning of a word'''
    # k = get_object_or_404(Kanji, kanji=kanji)

    # has_part = []
    # similar_sounded_kanji = []
    # used_as_radical = []

    # onyomi_list = k.onyomi.split('、')

    # similar_kanji = Kanji.objects.filter(parts__contains=k.kanji)

    # for s in similar_kanji:
    #     if s.kanji != k.kanji:
    #         if s.radical:
    #             if s.radical.radical==k.kanji:
    #                 used_as_radical.append(s.kanji)
    #             else:
    #                 has_part.append(s.kanji)
    #         else:
    #             has_part.append(s.kanji)
    #         for onyomi in onyomi_list:
    #             if onyomi in s.onyomi:
    #                 similar_sounded_kanji.append(s.kanji)
    #                 continue

    # context = {
    #     'kanji': k.kanji,
    #     'k_onyomi': k.onyomi,
    #     'k_kunyomi':k.kunyomi,
    #     'k_meaning':k.meaning,
    #     # 'k_examples': k.examples,
    #     'k_jlpt': k.jlpt_level,
    #     'radical': k.radical.radical,
    #     'r_meaning': k.radical.meaning,
    #     'r_readings': k.radical.readings,
    #     'parts':k.parts,
    #     # 'r_alternatives': k.radical.alternative,
    #     # 'kanji_by_radical': kanji_list,
    #     # 'similar_kanji_list':similar_kanji_list,
    #     # 'with_same_radical':with_same_radical,
    #     'has_part':has_part,
    #     'similar_sounded_kanji':similar_sounded_kanji,
    #     'used_as_radical':used_as_radical
    # }
    context, success = get_kanji_info(kanji)
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
