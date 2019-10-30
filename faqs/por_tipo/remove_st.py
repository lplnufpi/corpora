import re
from stopwords import stopwords

def get_index_last(i, words):
    if words[i].endswith('*'):
        return 1

filenames = ['como', 'direta', 'existe', 'o_que', 'por_que', 'posso', 'qual']

for filename in filenames:
    questions_no_stopwords = list()

    with open('./txt/{}.txt'.format(filename), 'r') as arq:
        text = arq.read()
        questions = text.split('\n')
        for quest in questions:
            type_id = re.search(r'_ (.*?) _', quest)
            no_type_id = re.sub(r'_ .*? _', 'TYPE_ID', quest)
            no_type_id = no_type_id.replace(',', '').replace('. ', '')
            no_type_id = no_type_id.replace('?', '')

            no_stopwords = list()
            words = no_type_id.split()

            while words:
                word = words.pop(0)
                if word.startswith('*'):
                    markeds = [word]
                    while words and not markeds[-1].endswith('*'):
                        markeds.append(words.pop(0))

                    # remove asteríscos
                    markeds[0] = markeds[0][1:]
                    markeds[-1] = markeds[-1][:-1]

                    markeds = [w for w in markeds if w not in stopwords]
                    no_stopwords.append('< {} >'.format(' '.join(markeds)))
                else:
                    if word not in stopwords:
                        no_stopwords.append(word)

            final_question = ' '.join(no_stopwords)
            if type_id is not None:
                final_question = final_question.replace(
                    'TYPE_ID', '_ {} _'.format(type_id.group(1))
                )

            questions_no_stopwords.append(final_question)

    with open('./no_stopwords/{}_no_st.txt'.format(filename), 'w') as arq:
        arq.write('\n'.join(questions_no_stopwords))