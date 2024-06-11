import re
import json
import random
import time
import numpy as np
import pandas as pd

from nlp_id import postag
from nlp_id import stopword
import nltk
nltk.download('punkt')

stopwords = stopword.StopWord()

dataset_CM = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='CM',
    engine='openpyxl',
    header=4
)

dataset_PM = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='PM',
    engine='openpyxl',
    # header=4
)

dataset_DTD = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='DTD',
    engine='openpyxl',
    # header=2
)

dataset_all = {
    'PM': dataset_PM,
    'CM': dataset_CM,
    'DTD': dataset_DTD
}

with open('./dataset/keywords.json') as key:
    keywords = json.load(key)

with open('./dataset/responses.json') as resp:
    responses = json.load(resp)

with open('./dataset/stack_text.json') as text:
    stack_text = json.load(text)


# def stack_text():
#     stack_text_all = {}
#     list_dataset = {
#         'CM': dataset_CM,
#         'PM': dataset_PM,
#         'DTD': dataset_DTD
#     }
#
#     for target in list_dataset.keys():
#         stack = " ".join([col.lower() for col in list_dataset[target].columns])
#
#         for words in keywords[target].keys():
#             for word in keywords[target][words]:
#                 stack += " " + word.lower()
#
#         for col in list_dataset[target].columns:
#             for statement in list_dataset[target][col].unique():
#                 for word in stopwords.remove_stopword(str(statement)).split(" "):
#                     stack += " " + word.lower()
#
#         stack_text_all[target] = stack
#
#     with open('./dataset/stack_text.json', 'w') as stack:
#         json.dump(stack_text_all, stack)
#
#     return stack_text_all


# Define a search function
def search_string(s, search):
    return search in str(s).lower()


def clean_text(message):
    final_text = []

    for word in message.split(' '):
        final_text.append(''.join(letter for letter in word if letter.isalnum()))

    return ' '.join(final_text)


def check_question(message):
    init = {
        'CM': 0,
        'PM': 0,
        'DTD': 0,
        'Wrong': 0
    }

    clean_message = stopwords.remove_stopword(message.replace("?", "").replace("|", ""))
    # clean_message = message.replace("?", "")

    for word in clean_message.split(" "):
        init_wrong = 0

        for target in init.keys():
            if target != 'Wrong':
                stack_text_all = stack_text[target] + stack_text_additional(target)
                if word.lower() in stack_text_all:
                    init[target] += 1
                    init_wrong += 1

        if init_wrong == 0:
            init['Wrong'] += 1

    # Step 1: Find the maximum value
    max_value = max(init.values())

    # Step 2: Find all keys that have this maximum value
    max_keys = [x for x, y in init.items() if y == max_value]

    kind_question = max_keys[0]

    return kind_question


def check_answering(message, target):
    init = {x: 0 for x in keywords[target].keys()}

    clean_message = clean_text(message)

    for word in clean_message.split(" "):
        for col in init.keys():
            if word.lower() in keywords[target][col]:
                init[col] += 1

    # Step 1: Find the maximum value
    max_value = max(init.values())

    # Step 2: Find all keys that have this maximum value
    max_keys = [x for x, y in init.items() if y == max_value]

    return max_keys[0]


# Streamed response emulator
def stream_response(message):
    for word in message.split():
        yield word + " "
        time.sleep(0.1)


def introduction_response():
    response = 'Hi saya Turbo-Doc, chatbot yang membantu menjawab pertanyaan seputar Suban Inlet GTC Titan-130.'
    for word in response.split():
        yield word + " "
        time.sleep(0.0001)


def wrong_response():
    response = random.choice([
        "Mohon untuk menulis kembali pertanyaan Anda yang sesuai dengan 3 pilihan di atas.",
        "Mohon untuk mengganti pertanyaan yang relevan dengan 3 pilihan diatas.",
        "Pertanyaan kamu diluar nalar kami. "
        "Mohon untuk mengubah pertanyaan yang relevan dengan 3 pilihan diatas.",
        "Maaf, pengetahuan kami belum sampai situ. "
        "Mohon untuk mengubah pertanyaan yang relevan sesuai dengan 3 pilihan diatas."
    ])

    return response


def stack_text_additional(type_question):
    stack_text_keywords = ''

    for a in keywords[type_question].keys():
        for b in keywords[type_question][a]:
            stack_text_keywords += ' ' + b

    return stack_text_keywords


def response_CM(type_question, filtered_question1, target_answering):
    target_question = ['Condition', 'Type', 'Tag Name', 'Description', 'Reason']
    target_col = ['Condition', 'Type', 'Tag Name', 'Description', 'Reason']
    target_data = []

    for col in target_col:
        for data in filtered_question1:
            data_stack = " ".join([str(val).lower() for val in dataset_CM[col].values])

            if data.lower() in data_stack and data.lower() not in target_data:
                target_data.append(data.lower())

                try:
                    target_question.remove(col)
                except:
                    pass

    filtered_df = None

    for i, word in enumerate(target_data):
        if i == 0:
            mask = dataset_CM.apply(lambda x: x.map(lambda s: search_string(s, word.lower())))
            filtered_df = dataset_CM.loc[mask.any(axis=1)]
        else:
            mask = filtered_df.apply(lambda x: x.map(lambda s: search_string(s, word.lower())))
            any_true = mask.values.any()

            if any_true:
                filtered_df = filtered_df.loc[mask.any(axis=1)]

    ind = filtered_df.index.values

    if len(ind) == 1:
        target_response = dataset_CM[target_answering][ind[0]]
        result_response = random.choice(responses[type_question][target_answering]) + ' ' + target_response
    else:
        additional_responses = '/'.join(target_question)
        result_response = random.choice([
            'Tolong spesifikkan pertanyaan Anda dengan memberikan informasi terkait ' + additional_responses + '.'
        ])

    return result_response


def response_PM(type_question, filtered_question1, target_answering):
    target_question = ['Task List', 'Frequency', 'Tools', 'Spare Part', 'Discipline']
    target_col = ['Task List', 'Frequency', 'Tools', 'Spare Part', 'Discipline']
    target_data = []

    for col in target_col:
        for data in filtered_question1:
            data_stack = " ".join([str(val).lower() for val in dataset_PM[col].values])

            if data.lower() in data_stack and data.lower() not in target_data:
                target_data.append(data.lower())

                try:
                    target_question.remove(col)
                except:
                    pass

    filtered_df = None

    for i, word in enumerate(target_data):
        if i == 0:
            mask = dataset_PM.apply(lambda x: x.map(lambda s: search_string(s, word.lower())))
            filtered_df = dataset_PM.loc[mask.any(axis=1)]
        else:
            mask = filtered_df.apply(lambda x: x.map(lambda s: search_string(s, word.lower())))
            any_true = mask.values.any()

            if any_true:
                filtered_df = filtered_df.loc[mask.any(axis=1)]

    ind = filtered_df.index.values

    if len(ind) == 1:
        target_response = dataset_PM[target_answering][ind[0]]
        result_response = random.choice(responses[type_question][target_answering]) + ' ' + target_response
    else:
        target_response = ''

        if target_answering == 'Frequency':
            target_response = dataset_PM[target_answering][ind[0]]
        elif target_answering == 'Task List':
            target_response = ''.join([f'({i + 1}) {word} \n' for i, word in enumerate(dataset_PM[target_answering].iloc[ind])])

        additional_responses = '/'.join(target_question)
        result_response = random.choice([
            'Tolong spesifikkan pertanyaan Anda dengan memberikan informasi terkait ' +
            additional_responses +
            ' . Namun, karena keterbatasan sistem, kami coba bantu dengan jawaban seperti ini. ' +
            random.choice(responses[type_question][target_answering]) +
            target_response + '.'
        ])

    return result_response


def response_DTD(type_question, last_message):
    target_response = dataset_DTD[dataset_DTD['Question'].str.contains(last_message)]['Answer'].values[0]
    result_response = random.choice(responses[type_question]['Answer']) + ' ' + target_response

    return result_response


def generate_response(message):
    type_question = check_question(message)

    if type_question != 'Wrong':
        last_message = message.split("|")[-1]

        postagger = postag.PosTag()
        tag_question1 = postagger.get_phrase_tag(message)
        tag_question2 = postagger.get_phrase_tag(last_message)

        # print(tag_question1)

        filtered_question1 = [item[0] for item in tag_question1 if (item[1] == 'NP' or
                                                                    item[1] == 'NNP' or
                                                                    item[1] == 'DP' or
                                                                    item[1] == 'NN' or
                                                                    item[1] == 'NUM')]
        filtered_question2 = [item[0] for item in tag_question2 if (item[1] == 'NP' or
                                                                    item[1] == 'NNP' or
                                                                    item[1] == 'DP' or
                                                                    item[1] == 'NN' or
                                                                    item[1] == 'NUM')]

        type_answering = check_answering(last_message, type_question)
        target_answering = ''

        if type_question == 'CM':
            target_answering = response_CM(type_question, filtered_question1, type_answering)
        elif type_question == 'PM':
            target_answering = response_PM(type_question, filtered_question1, type_answering)
        elif type_question == 'DTD':
            target_answering = response_DTD(type_question, last_message)

        return target_answering

    else:
        return wrong_response()
