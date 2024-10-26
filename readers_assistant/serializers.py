from sudachipy import tokenizer
from sudachipy import dictionary
from jmdict.models import Dictionary_Entry, Sense, Example
from rest_framework_mongoengine.serializers import DocumentSerializer, EmbeddedDocumentSerializer

tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
# modeA = tokenizer.Tokenizer.SplitMode.A
# modeB = tokenizer.Tokenizer.SplitMode.B
modeC = tokenizer.Tokenizer.SplitMode.C


class ExampleSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Example
        depth = 2
        fields = ('ex_sent_jpn', 'ex_sent_eng')


class SenseSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Sense
        depth = 2
        fields = ('pos', 'meaning', 'example')


class VocabSerializer(DocumentSerializer):
    class Meta:
        model = Dictionary_Entry
        depth = 2
        fields = ('k_ele', 'r_ele', 'sense')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        s_c = 0
        for sense in instance['sense']:
            e_c = 0
            for example in sense['example']:
                sen_token = tokenizer_obj.tokenize(example['ex_sent_jpn'], modeC)
                sent_dic = {}
                for tok in sen_token:
                    sent_dic[str(tok)]=tok.dictionary_form()
                representation['sense'][s_c]['example'][e_c]['tokens']=sent_dic
                e_c+=1
            s_c+=1
        return representation
