from .models import Kanji

def get_kanji_info(word):
    try:
        k = Kanji.objects.get(kanji=word[0])

        share_same_radical = []
        if k.radical and k.kanji != k.radical.radical:
            same_radical = Kanji.objects.filter(radical=k.radical).defer(
                'kanji').order_by('jlpt_level')
            # print(same_radical)
            for r in same_radical:
                share_same_radical.append(r.kanji)

        similar_kanji = Kanji.objects.filter(parts__contains=k.kanji)
        # print(similar_kanji)
        parts = [p for p in k.parts.split(',') if p != k.kanji]
        has_part = []
        share_same_onyomi = []
        used_as_radical = []

        onyomi_list = k.onyomi.split('、')
        for s in similar_kanji:
            if s.kanji != k.kanji:
                if s.radical:
                    if s.radical.radical==k.kanji:
                        used_as_radical.append(s.kanji)
                    else:
                        has_part.append(s.kanji)
                else:
                    has_part.append(s.kanji)
                for onyomi in onyomi_list:
                    if onyomi in s.onyomi:
                        if s.kanji not in share_same_onyomi:
                            share_same_onyomi.append(s.kanji)
                        continue
        context = {
            'word':word,
            'kanji': k.kanji,
            'k_onyomi': k.onyomi,
            'k_kunyomi':k.kunyomi,
            'k_meaning':k.meaning,
            'k_parts':parts,
            'k_examples': k.examples,
            'k_jlpt': k.jlpt_level,
            'radical': k.radical.radical if k.radical else '',
            'r_meaning': k.radical.meaning if k.radical else '',
            'r_readings': k.radical.readings if k.radical else '',
            'r_alternatives': k.radical.alternative if k.radical else '',
            'share_same_radical': share_same_radical,
            'share_same_onyomi':share_same_onyomi,
            'has_part':has_part,
            'used_as_radical':used_as_radical,
        }
        return context, True
    except Kanji.DoesNotExist:
        return {}, False