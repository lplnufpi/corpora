import re
import nlpnet

filenames = ['como', 'direta', 'existe', 'o_que', 'por_que', 'posso', 'qual']
nlpnet.set_data_dir('/home/jpegx100/develop/lpln/pos-pt')
tagger = nlpnet.POSTagger()

for filename in filenames:
    tagged_questions = list()

    with open('./no_stopwords/{}_no_st.txt'.format(filename), 'r') as arq:
        text = arq.read()
        questions = text.split('\n')
        for quest in questions:
            # type_id = re.search(r'_ (.*?) _', quest)
            # no_type_id = re.sub(r'_ .*? _', 'TYPE_ID', quest)
            no_type_id = quest

            tagged_question = list()
            words = no_type_id.split()

            while words:
                word = words.pop(0)
                if word == '_':
                    tagged_question.append('_')
                    continue
                if word.startswith('*'):
                    markeds = [word]
                    while words and not markeds[-1].endswith('*'):
                        markeds.append(words.pop(0))

                    # remove asteríscos
                    markeds[0] = markeds[0][1:]
                    markeds[-1] = markeds[-1][:-1]
                    tags = tagger.tag(' '.join(markeds))
                    if tags:
                        joined = ' '.join(['/'.join(x) for x in tags[0]])
                        tagged_question.append('*{}*'.format(joined))
                else:
                    tags = tagger.tag(word)
                    joined = ' '.join(['/'.join(x) for x in tags[0]])
                    tagged_question.append(joined)

            final_question = ' '.join(tagged_question)
            # if type_id is not None:
            #     final_question = final_question.replace(
            #         'TYPE_ID', '_ {} _'.format(type_id.group(1))
            #     )

            tagged_questions.append(final_question)

    with open('./tagged/{}_tagged.txt'.format(filename), 'w') as arq:
        arq.write('\n'.join(tagged_questions))