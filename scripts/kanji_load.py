import csv

from django.shortcuts import get_object_or_404
from kanji.models import Radical, Kanji


def run():
    kan = open('scripts/kanji.csv')
    rad = open('scripts/radicals.csv')

    reader_kan = csv.reader(kan)
    reader_rad = csv.reader(rad)
    next(reader_kan, None)
    next(reader_rad, None)

    Radical.objects.all().delete()
    Kanji.objects.all().delete()

    for row in reader_rad:
        rad = row[0]
        rad_no = row[1]
        nos = row[2]
        alt = row[3]
        m = row[4]
        read = row[5]
        # print(rad, rad_no, nos, alt, m, read)

        r = Radical(radical=rad, radical_number=rad_no, number_of_stroke=nos, alternative=alt, meaning=m, readings=read)
        r.save()

    for row in reader_kan:
        # print(row)

        kan = row[1]
        on = row[2]
        kun = row[3]
        m = row[4]
        ex = row[5]
        jlpt = row[6]
        nos = row[7]
        rad = row[8]
        # print(kan, on, kun, m, ex, jlpt, nos, rad)

        r = None
        try:
            r = Radical.objects.get(radical=rad)
        except:
            r = None

        k = Kanji(kanji=kan, onyomi=on, kunyomi=kun, meaning=m, examples=ex, jlpt_level=jlpt, no_of_strokes=nos,
                  radical=r)
        k.save()


