from kanji.models import Radical, Kanji

def run():

    kanji = Kanji.objects.get(kanji='深')
    kanji.parts = '儿, 冖, 汁, 木'
    # radical = Radical.objects.get(radical='攵')
    # kanji.radical = radical
    kanji.save()
    