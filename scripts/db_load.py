import json
from mongoengine import *
from jmdict.models import Example, Sense, Dictionary_Entry

connect('jmdict')
# Dictionary_Entry.drop_collection()
def run():
    with open('scripts/data.json') as file:
        file_data = json.load(file)

    words = file_data['JMdict']['entry']
    count = 0
    def get_k_ele(k_ele):
        kanji = []
        if isinstance(k_ele, list):
            for ele in k_ele:
                kanji.append(ele.get('keb'))
                # print(ele.get('keb'))
        elif isinstance(k_ele, dict):
            kanji.append(k_ele.get('keb'))
            # print(k_ele.get('keb'))
        return kanji

    def get_r_ele(r_ele):
        romaji = []
        if isinstance(r_ele, list):
            for ele in r_ele:
                romaji.append(ele.get('reb'))
                # print(ele.get('reb'))
        elif isinstance(r_ele, dict):
            romaji.append(r_ele.get('reb'))
            # print(r_ele.get('reb'))
        return romaji

    def get_pos(sense):
        pos_list = []
        pos = sense.get('pos')
        if isinstance(pos, list):
            for ele in pos:
                pos_list.append(ele)
                # print(ele.get('reb'))
        elif isinstance(pos, dict):
            pos_list.append(pos)
            # print(r_ele.get('reb'))
        return pos_list

    def get_sense(sense):
        senses = []
        if isinstance(sense, list):
            for sen in sense:
                # print('POS')
                sense_dict = {}
                sense_dict['pos'] = get_pos(sen)
                sense_dict['gloss'] = get_gloss(sen)
                # print(sen.get('pos'))
                # get_gloss(sen)
                sense_dict['example'] = get_example(sen)
                # print(sense_dict)
                sense_obj = Sense(pos=sense_dict['pos'], meaning=sense_dict['gloss'],
                                  example=sense_dict['example'])
                # sense_obj.save()

                senses.append(sense_obj)
        elif isinstance(sense, dict):
            # print(sense.get('pos'))
            sense_dict = {}
            sense_dict['pos'] = get_pos(sense)
            sense_dict['gloss'] = get_gloss(sense)
            # get_gloss(sense)
            sense_dict['example'] = get_example(sense)
            sense_obj = Sense(pos=sense_dict['pos'], meaning=sense_dict['gloss'],
                                example=sense_dict['example'])
            # sense_obj.save()
            senses.append(sense_obj)
        return senses

    def get_example(sen):
        examples = []
        example_dict = {}
        example = sen.get('example')
        if example:
            # print(example.get('ex_text'))
            if isinstance(example, list):
                for exem in example:
                    example_dict['ex_text'] = exem.get('ex_text')
                # ex_sentences = []
                ex_sent = exem.get('ex_sent')
                for ex in ex_sent:
                    # print(ex)
                    if ex.get('@xml:lang') == 'jpn':
                        example_dict['ex_sent_jpn'] = ex.get('#text')
                    elif ex.get('@xml:lang') == 'eng':
                        example_dict['ex_sent_eng'] = ex.get('#text')
                    # ex_sentences.append(ex)
                # example_dict['ex_sent'] = ex_sentences
                example_obj = Example(ex_text = example_dict['ex_text'], ex_sent_jpn=example_dict['ex_sent_jpn'],
                                    ex_sent_eng=example_dict['ex_sent_eng'])
                examples.append(example_obj)
            elif isinstance(example, dict):
                example_dict['ex_text'] = example.get('ex_text')
                # ex_sentences = []
                ex_sent = example.get('ex_sent')
                for ex in ex_sent:
                    # print(ex)
                    if ex.get('@xml:lang') == 'jpn':
                        example_dict['ex_sent_jpn'] = ex.get('#text')
                    elif ex.get('@xml:lang') == 'eng':
                        example_dict['ex_sent_eng'] = ex.get('#text')
                    # ex_sentences.append(ex)
                # example_dict['ex_sent'] = ex_sentences
                example_obj = Example(ex_text = example_dict['ex_text'], ex_sent_jpn=example_dict['ex_sent_jpn'],
                                    ex_sent_eng=example_dict['ex_sent_eng'])
                examples.append(example_obj)
            # example_obj.save()
        return examples

    def get_gloss(sen):
        gloss = sen.get('gloss')
        gloss_list =[]
        if isinstance(gloss, list):
            for gl in gloss:
                # print(gl.get('#text'))
                gloss_list.append(gl.get('#text'))
        elif isinstance(gloss, dict):
            gloss_list.append(sen.get('gloss').get('#text'))
            # print(sen.get('gloss').get('#text'))
        return gloss_list
    # count=0
    for word in words:
        word_desc = {}
        word_desc['ect_seq'] = word['ent_seq']
        # print(word['ent_seq'])
        k_ele = word.get('k_ele')
        if k_ele:
            # print('Kanji Element')
            word_desc['k_ele'] = get_k_ele(k_ele)
        r_ele = word.get('r_ele')
        if r_ele:
            # print('Romaji Element')
            word_desc['r_ele'] = get_r_ele(r_ele)
        sense = word.get('sense')
        if sense:
            # print('Sense')
            word_desc['sense'] = get_sense(sense)

            # print(example.get('ex_text'))
            # print(example.get('ex_sent'))

        # if count>140000:
        #     print(count)
        # count+=1
        vocabulary = Dictionary_Entry(entry=word_desc['ect_seq'], k_ele=word_desc.get('k_ele'),
                                        r_ele=word_desc.get('r_ele'), sense=word_desc['sense'])
        vocabulary.save()
