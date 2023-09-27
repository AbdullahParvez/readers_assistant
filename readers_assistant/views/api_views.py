# from rest_framework.generics import GenericAPIView
from rest_framework_mongoengine.generics import ListAPIView
from ..serializers import VocabSerializer
from jmdict.models import Dictionary_Entry
# from rest_framework.response import Response

from mongoengine import *
from mongoengine.queryset.visitor import Q

connect('jmdict')


# def get_word_details(vocab):
#     '''retrieve and rearrange meaning of a word'''
#     results = Dictionary_Entry.objects(Q(k_ele__exact=vocab)|Q(r_ele__exact=vocab))
#     meanings = []
#     count = 1
#     for res in results:
#         meaning = {}
#         meaning['no'] = count
#         meaning['k_ele'] = ', '.join(res.k_ele)
#         meaning['r_ele'] = res.r_ele
#         m_sense=[]
#         sense = res.sense
#         for se in sense:
#             temp = {}
#             temp['meaning']=se.meaning
#             temp['pos']=se.pos
#             m_sense.append(temp)
#             example = se.example
#             examples = []
#             for ex in example:
#                 tmp = {}
#                 if ex.ex_text == vocab:
#                     tmp['ex_sent_jpn'] = ex.ex_sent_jpn
#                     tmp['ex_sent_eng'] = ex.ex_sent_eng
#                     examples.append(tmp)
#             temp['examples'] = examples
#         meaning['sense'] = m_sense
#         meanings.append(meaning)
#         count +=1
#     return meanings


class GetVocabDetails(ListAPIView):
    """
    Return vocab details.
    """
    serializer_class = VocabSerializer

    def get(self, request, vocab, *args, **kwargs):
        self.queryset = Dictionary_Entry.objects(Q(k_ele__exact=vocab)|Q(r_ele__exact=vocab))
        return self.list(request, *args, **kwargs)
    
    # def get(self, request, vocab, format=None):
    #     # vocab = self.kwargs['vocab']
    #     meanings = get_word_details(vocab=vocab)
    #     results = Dictionary_Entry.objects(Q(k_ele__exact=vocab)|Q(r_ele__exact=vocab))
    #     print(results)
    #     serializer = self.get_serializer(data=results[0])
    #     if serializer.is_valid():
    #         return Response(serializer.data)
    #     return Response(serializer.errors,status=400)
