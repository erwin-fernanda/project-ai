import numpy as np
import pandas as pd
import json
import random
import time

from nlp_id.postag import PosTag
from nlp_id.lemmatizer import Lemmatizer
from nlp_id.stopword import StopWord

stopword = StopWord()

dataset_CM = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='CM',
    header=4
)

dataset_PM = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='PM',
    # header=4
)

dataset_DTD = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='DTD',
    # header=2
)


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
#                 for word in stopword.remove_stopword(str(statement)).split(" "):
#                     stack += " " + word.lower()
#
#         stack_text_all[target] = stack
#
#     with open('./dataset/stack_text.json', 'w') as stack:
#         json.dump(stack_text_all, stack)
#
#     return stack_text_all


def check_question(message):
    clean_message = stopword.remove_stopword(message)
    print(clean_message)

    for word in clean_message.split(" "):
        if word.lower() in stack_text['CM']:
            return 'CM'
        elif word.lower() in stack_text['PM']:
            return 'PM'
        elif word.lower() in stack_text['DTD']:
            return 'DTD'
        else:
            return 'Wrong'


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


def response_CM(message):
    response = "CM"

    return response


def response_PM(message):
    response = "PM"

    return response


def response_DTD(message):
    response = "DTD"

    return response


def generate_response(message):
    kind_question = check_question(message)
    if kind_question == 'CM':
        return response_CM(message)
    elif kind_question == 'PM':
        return response_PM(message)
    elif kind_question == 'DTD':
        return response_DTD(message)
    else:
        return wrong_response()

