import numpy as np
import pandas as pd
from nlp_id.postag import PosTag
from nlp_id.lemmatizer import Lemmatizer
import random
import time

dataset_1 = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='CM',
    header=4
)

dataset_2 = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='DTD',
    header=2
)

kind_of_question = {
    'Reason': [
        'kenapa',
        'penyebab',
        'mengapa',
        'reason',
        'cause',
        'why',
        'menyebabkan',
        'sebab',
        'terjadi'
    ],
    'General Recommendation': [
        'rekomendasi',
        'saran',
        'advice',
        'mengatasi',
        'menyelesaikan',
        'cara',
        'atasi',
        'solusi',
        'selesai',
        'rekomendasinya',
        'mengatasinya',
        'caranya',
        'sarannya'
    ],
    'Specific Recommendation': [
        'spare-part',
        'spare part',
        'part',
        'dibutuhkan',
        'bagian',
        'komponen',
        'spare-partnya',
        'sparepart',
        'spares',
        'parts',
        'spare'
    ]
}


first_statement = {
    'Reason': random.choice([
        'Hal itu bisa terjadi karena',
        'Penyebabnya adalah',
        'Salah satu penyebabnya adalah',
        'Hal itu terjadi karena',
        'Hal itu disebabkan oleh',
        'Penyebab dari masalah itu adalah'
    ]),
    'General Recommendation': random.choice([
        'Saya bisa merekomendasikan langkah-langkah yang bisa dilakukan sebagai berikut: \n',
        'Anda bisa melakukan hal-hal sebagai berikut: \n',
        'Anda bisa menerapkan langkah-langkah berikut ini: \n',
        'Advice dari saya untuk masalah ini adalah sebagai berikut: \n',
        'Cara untuk menyelesaikan masalah ini yang bisa dicoba sebagai berikut: \n',
    ]),
    'Specific Recommendation': random.choice([
        'Rekomendasi part number spare-part SOLAR yang bisa digunakan adalah sebagai berikut: \n',
        'Anda bisa menggunakan SOLAR part number sebagai berikut: \n',
        'Spare-part SOLAR yang sudah mulai harus dipersiapkan adalah \n',
    ])
}


def check_question_residual(filtered_question):
    draft_question = []

    check_df_type = dataset_1['Type'].str.contains('|'.join(filtered_question), case=False)
    check_df_tag = dataset_1['Tag Name'].str.contains('|'.join(filtered_question), case=False)
    check_df_description = dataset_1['Description'].str.contains('|'.join(filtered_question), case=False)

    if True in check_df_type.values:
        draft_question.append('Type')

    if True in check_df_tag.values:
        draft_question.append('Tag Name')

    if True in check_df_description.values:
        draft_question.append('Description')

    return draft_question


def check_question_general(question):
    for word in question.split(" "):
        if word.lower() in kind_of_question['Reason']:
            return 'Reason'
        elif word.lower() in kind_of_question['General Recommendation']:
            return 'General Recommendation'
        elif word.lower() in kind_of_question['Specific Recommendation']:
            return 'Specific Recommendation'


def stack_text(dataset_1):
    stack = " ".join([col.lower() for col in dataset_1.columns])

    for words in kind_of_question.keys():
        for word in kind_of_question[words]:
            stack += " " + word.lower()

    stack += "mungkin"

    for col in dataset_1.columns:
        for statement in dataset_1[col].unique():
            for word in str(statement).split(" "):
                stack += " " + word.lower()

    return stack


def check_wrong_question(question):
    stack_sentences = stack_text(dataset_1)
    init = 0

    for word in question.split(" "):
        if word.lower() in stack_sentences:
            init += 1

    if init == 0:
        return False
    else:
        return True


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


def random_response():
    response = random.choice([
        "Tolong ubah pertanyaanmu",
        "Maksud kamu apa, ya?",
        "Tolong ganti pertanyaan yang relevan",
        "Pertanyaan kamu diluar nalar kami",
        "Maaf, pengetahuan kami belum sampai situ"
    ])
    for word in response.split():
        yield word + " "
        time.sleep(0.1)


def generate_response(question):
    message_forward = ''
    
    postagger = PosTag()
    tag_question1 = postagger.get_phrase_tag(question)
    tag_question2 = postagger.get_phrase_tag(question.split(" || ")[-1])
    filtered_question = [item[0] for item in tag_question1 if (item[1] == 'NP' or item[1] == 'NNP' or
                                                               item[1] == 'DP')]
    filtered_question1 = [item[0] for item in tag_question2 if (item[1] == 'NP' or item[1] == 'NNP' or
                                                                item[1] == 'DP')]
    lemmatizer = Lemmatizer()
    target_question = check_question_general((lemmatizer.lemmatize(question.split(" || ")[-1])))
    draft_question = check_question_residual(filtered_question)
    check_question = check_wrong_question(" ".join(filtered_question1))
    print(check_question)

    if 'Type' in draft_question:
        if 'Tag Name' in draft_question and 'Description' in draft_question and check_question:
            dataset_final = dataset_1[
                (dataset_1['Tag Name'].str.contains('|'.join(filtered_question), case=False) &
                 dataset_1['Description'].str.contains('|'.join(filtered_question), case=False)) &
                dataset_1['Type'].str.contains('|'.join(filtered_question), case=False)
            ]

            message_forward = first_statement[target_question] + ' ' + dataset_final[target_question].values[0]

        elif 'Tag Name' in draft_question and check_question:
            dataset_final = dataset_1[
                dataset_1['Tag Name'].str.contains('|'.join(filtered_question), case=False) &
                dataset_1['Type'].str.contains('|'.join(filtered_question), case=False)
            ]

            message_forward = first_statement[target_question] + ' ' + dataset_final[target_question].values[0]

        elif 'Description' in draft_question and check_question:
            dataset_final = dataset_1[
                dataset_1['Description'].str.contains('|'.join(filtered_question), case=False) &
                dataset_1['Type'].str.contains('|'.join(filtered_question), case=False)
            ]

            message_forward = first_statement[target_question] + ' ' + dataset_final[target_question].values[0]

        else:
            message_forward = random.choice([
                'Tolong spesifikkan tag name atau deskripsi yang lebih rinci',
                'Bisa dituliskan tag name yang bermasalah?',
                'Bisa disebutkan tag name yang bermasalah?',
                'Tolong tuliskan lebih rinci untuk spesifikasi tag name atau deskripsinya'
            ])

    elif 'Type' not in draft_question:
        if ('Tag Name' in draft_question or 'Description' in draft_question) and check_question:
            dataset_final = dataset_1[
                (dataset_1['Tag Name'].str.contains('|'.join(filtered_question), case=False) |
                 dataset_1['Description'].str.contains('|'.join(filtered_question), case=False))
            ]

            if len(dataset_final) != 1:
                message_forward = random.choice([
                    'Mohon spesifikkan kode alarm/shutdown muncul.',
                    'Mohon untuk menuliskan kondisi alarm/shutdown yang muncul'
                ])
            else:
                message_forward = first_statement[target_question] + ' ' + dataset_final[target_question].values[0]

        else:
            message_forward = random.choice([
                "Mohon untuk menulis kembali pertanyaan Anda yang sesuai dengan 3 pilihan di atas.",
                "Mohon untuk mengganti pertanyaan yang relevan dengan 3 pilihan diatas.",
                "Pertanyaan kamu diluar nalar kami. "
                "Mohon untuk mengubah pertanyaan yang relevan dengan 3 pilihan diatas.",
                "Maaf, pengetahuan kami belum sampai situ. "
                "Mohon untuk mengubah pertanyaan yang relevan sesuai dengan 3 pilihan diatas."
            ])

    return message_forward

