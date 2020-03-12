import re
import nlpnet
from por_tipo.stopwords import stopwords

filename = 'aspects'
nlpnet.set_data_dir('/home/jpegx100/develop/lpln/pos-pt')
tagger = nlpnet.POSTagger()

tagged_questions = list()

with open('{}.txt'.format(filename), 'r') as arq:
    text = arq.read().split(' ')
    text = [t for t in text if t not in stopwords]
    questions = ' '.join(text).split('\n')

    for quest in questions:

        tags = tagger.tag(quest)
        joined = ' '.join([y for (x, y) in tags[0]])

        spcs = ' --- '# * (60 - len(joined))
        final_question = joined + spcs + quest.strip()
        tagged_questions.append(final_question)

with open('{}_tagged.txt'.format(filename), 'w') as arq:
    tagged_questions.sort()
    arq.write('\n'.join(tagged_questions))




arq = open('{}_tagged.txt'.format(filename), 'r')
lines = arq.read().split('\n')
arq.close()

dicionario = {}
for line in lines:
    tag = line.split(' --- ')[0]
    if tag in dicionario:
            dicionario[tag] = dicionario[tag] + 1
    else:
            dicionario[tag] = 1

new_lines = list()
for (x, y) in dicionario.items():
    spcs = ' ' * (60 - len(x))
    new_lines.append('{} {} {}'.format(x, spcs, y))

def compare(item1, item2):
    a = int(item1.split('   ')[-1])
    b = int(item2.split('   ')[-1])
    return b-a

import functools
new_lines = sorted(new_lines, key=functools.cmp_to_key(compare))

with open('{}_tagged_count.txt'.format(filename), 'w') as arq:
    arq.write('\n'.join(new_lines))