from function import generator_responses as gr
import pandas as pd
from nlp_id.postag import PosTag
from nlp_id.lemmatizer import Lemmatizer


dataset_1 = pd.read_excel(
    'dataset/dataset_turbo-doc.xlsx',
    sheet_name='Table CM',
    header=4
)


# print(dataset_1.columns)
question = 'Kenapa AL_AF0291_Calib_Fault terjadi?'

postagger = PosTag()
tag_question1 = postagger.get_phrase_tag(question)
filtered_question1 = [item[0] for item in tag_question1 if (item[1] == 'NP' or item[1] == 'NNP' or
                                                            item[1] == 'DP' or item[1] == 'VP' or
                                                            item[1] == 'NN')]

stack_statement = gr.check_wrong_question(" ".join(filtered_question1))
print(stack_statement)
print(filtered_question1)
