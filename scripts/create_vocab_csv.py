import csv
import json

from django.shortcuts import get_object_or_404
from kanji.models import Radical, Kanji


def run():
    n5_vocab = open('scripts/n1_vocab.csv')

    reader_vocab = csv.reader(n5_vocab)
    next(reader_vocab, None)
    radical_dic = {}
    word_count = 0
    for row in reader_vocab:
        letters = row[0]
        # print(letters)
        if letters:
            for letter in letters:
                try:
                    kanji = Kanji.objects.get(kanji=letter)
                    if kanji:
                        if kanji.radical.radical in radical_dic:
                            word_count += 1
                            radical_dic[kanji.radical.radical].append(
                                [kanji.kanji, row[1], row[0], row[2]])
                        else:
                            radical_dic[kanji.radical.radical] = [
                                [kanji.kanji, row[1], row[0], row[2]]]
                            word_count += 1

                except Exception as exp:
                    pass
        else:
            # print(row[1])
            if 'other' in radical_dic:
                radical_dic['other'].append(['', row[1], row[1], row[2]])
                word_count += 1
            else:
                radical_dic['other'] = [['', row[1], row[1], row[2]]]
                word_count += 1
    # print(len(radical_dic['other']))
    # print(word_count)

    vocab_db = {}
    # level = 1
    unit_no = 1
    set_no = 1
    # vocab_count = 0
    word_count = 10001
    unit_count = 101
    set_count = 1001

    set_vocab_list = []

    radicals = Radical.objects.all().order_by('radical_number')
    for radical in radicals:
        # print(radical.radical_number)
        if radical.radical in radical_dic:
            vocabs = radical_dic[radical.radical]
            for vocab in vocabs:
                unit = 'unit_'+str(unit_no)
                set = 'set_'+str(set_no)
                if unit in vocab_db:
                    if set in vocab_db[unit]['sets']:
                        if vocab[2] in set_vocab_list:
                            print(vocab[2])
                            continue
                        vocab_db[unit]['sets'][set]['vocabs'].append({
                            'id': word_count,
                            'word': vocab[2],
                            'pronunciation': vocab[1],
                            'meaning': vocab[3],
                            'radical': radical.radical,
                            'kanji': vocab[0]
                        })
                        set_vocab_list.append(vocab[2])
                        word_count += 1
                    else:
                        vocab_db[unit]['sets'][set] = {
                            'id': set_count,
                            'vocabs':[]
                        }
                        # vocab_db[unit][set]['vocabs'] = []
                        vocab_db[unit]['sets'][set]['vocabs'].append({
                            'id': word_count,
                            'word': vocab[2],
                            'pronunciation': vocab[1],
                            'meaning': vocab[3],
                            'radical': radical.radical,
                            'kanji': vocab[0]
                        })
                        set_vocab_list.append(vocab[2])
                        word_count += 1
                    # vocab_db[unit][set][vocab[2]]=[radical.radical, vocab[0], vocab[1], vocab[3],word_count]

                else:
                    vocab_db[unit] = {
                        'id': unit_count,
                        'sets':{}
                    }
                    vocab_db[unit]['sets'][set] = {
                        'id': set_count,
                        'vocabs':[]
                    }
                    # vocab_db[unit][set]['vocabs'] = []
                    vocab_db[unit]['sets'][set]['vocabs'].append({
                        'id': word_count,
                        'word': vocab[2],
                        'pronunciation': vocab[1],
                        'meaning': vocab[3],
                        'radical': radical.radical,
                        'kanji': vocab[0]
                    })
                    set_vocab_list.append(vocab[2])
                    word_count += 1
                    # vocab_db[unit][set]=[[radical.radical, vocab[0], vocab[1],vocab[2], vocab[3]]]

                # vocab_count += 1
                # print(len(set_vocab_list))
                if len(set_vocab_list) == 20:
                    set_count+=1
                    set_no += 1
                    # print(word_count)
                    # print(set_vocab_list)
                    set_vocab_list = []
                    if set_no == 26:
                        unit_count+=1
                        unit_no += 1
                        set_no = 1

    other_vocabs = radical_dic['other']
    for vocab in other_vocabs:
        unit = 'unit_'+str(unit_no)
        set = 'set_'+str(set_no)
        if unit in vocab_db:
            if set in vocab_db[unit]['sets']:
                if vocab[2] in set_vocab_list:
                    continue
                # vocab_db[unit][set][vocab[2]] = [
                #     '', vocab[0], vocab[1], vocab[3]]
                vocab_db[unit]['sets'][set]['vocabs'].append({
                    'id': word_count,
                    'word': vocab[2],
                    'pronunciation': vocab[1],
                    'meaning': vocab[3],
                    'radical': '',
                    'kanji': vocab[0]
                })
                set_vocab_list.append(vocab[2])
                word_count += 1
            else:
                vocab_db[unit]['sets'][set] = {
                    'id': set_count,
                    'vocabs':[]
                }
                vocab_db[unit]['sets'][set]['vocabs'].append({
                    'id': word_count,
                    'word': vocab[2],
                    'pronunciation': vocab[1],
                    'meaning': vocab[3],
                    'radical': '',
                    'kanji': vocab[0]
                })
                set_vocab_list.append(vocab[2])
                word_count += 1
                # vocab_db[unit][set][vocab[2]] = [
                #     '', vocab[0], vocab[1], vocab[3]]

        else:
            vocab_db[unit] = {
                'id': unit_count,
                'sets':{}
            }
            vocab_db[unit]['sets'][set] = {
                'id': set_count,
                'vocabs':[]
            }
            vocab_db[unit]['sets'][set]['vocabs'].append({
                'id': word_count,
                'word': vocab[2],
                'pronunciation': vocab[1],
                'meaning': vocab[3],
                'radical': '',
                'kanji': vocab[0]
            })
            set_vocab_list.append(vocab[2])
            word_count += 1
            # vocab_db[unit][set][vocab[2]] = ['', vocab[0], vocab[1], vocab[3]]

        # vocab_count += 1
        # word_count += 1
        if len(set_vocab_list) == 20:
            set_count+=1
            set_no += 1
            set_vocab_list = []
            if set_no == 26:
                unit_count+=1
                unit_no += 1
                set_no = 1
            # vocab_count = 0

    vocab_db = [vocab_db]
    radical_dic = [radical_dic]

    json_object = json.dumps(vocab_db, indent=4, ensure_ascii=False)
    # json_object_2 = json.dumps(radical_dic, indent=4, ensure_ascii=False)

    # Writing to sample.json
    with open("scripts/n1_vocab_data.json", "w") as outfile:
        outfile.write(json_object)

    # with open("scripts/n5_vocab.json", "w") as outfile:
    #     outfile.write(json_object_2)
