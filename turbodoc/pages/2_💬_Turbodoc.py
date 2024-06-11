import os
import time
import random
from PIL import Image
from function import generator_responses as gr

import streamlit as st
from streamlit import session_state as state

st.set_page_config(
    page_title="Turbo-Doc App",
    page_icon="💬",
)

if 'login' not in list(state.keys()):
    state['login'] = False

state['start'] = True

image = Image.open(f'./image/logo_skk_migas.png')

sta, stb, stc = st.columns(3)

with stb:
    st.image(image)

st.markdown('<h3 style="text-align: center;">Turbodoc Application</h3>', unsafe_allow_html=True)

if state['login']:
    with st.sidebar:
        intro = "Aplikasi Turbo-Doc ini dibangun dengan menggunakan dataset yang sudah diprovide oleh tim " \
                "engineer <b>Suban Inlet GTC Titan-130</b> yang sudah berpengalaman untuk menjawab masalah berikut ini"\
                ":<br> <br> 1. <b>Preventive Maintenance-PM</b> (Task list, Spare Part, Tools, Jadwal, Jenis). <br>" \
                "2. <b>Corrective Maintenance-CM</b> (Troubleshooting, Rekomendasi Spare Part untuk Masalah Tertentu, "\
                "Langkah-Langkah Troubleshooting untuk Suatu Alarm/Shutdown Tertentu). <br>" \
                "<b>Catatan:</b> Tolong tuliskan juga kode alarm/shutdown-nya. <br>" \
                "3. Seputar masalah <b>day to day operation Suban GTC Inlet</b>. <br> <br>" \
                "Kemudian dataset akan dilatih dengan menggunakan model <b>Deep Learning</b> berbasis <b>NLP</b> " \
                "menggunakan python. Adapun untuk member yang terlibat di projek ini: <br> <br>" \
                "1. <b> Eira P. Arief </b> (Project Manager) <br>" \
                "2. <b> Desta Afianto </b> (Domain Expertise) <br>" \
                "3. <b> Sani Dadan </b> (Domain Expertise) <br>" \
                "4. <b> Enrill Tommy F. </b> (Domain Expertise) <br>" \
                "5. <b> Erwin Fernanda </b> (Data and ML Engineer) <br>"

        st.title("Introduction")
        st.markdown(f'<div style="text-align: justify;">{intro}</div>', unsafe_allow_html=True)

    # Initialize chat history and question
    if "messages" not in state:
        state.messages = []

        st1, st2 = st.columns(2)

        with st1:
            with st.chat_message("assistant"):
                st.write_stream(gr.introduction_response())

    if 'question' not in state:
        state.question = ''

    margin = [st.columns(2) for i in range(len(state.messages))]

    # Display chat messages from history on app rerun
    for j, message in enumerate(state.messages):
        if message["role"] == 'user':
            init = 1
        else:
            init = 0

        with margin[j][init]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Messages Turbo-Doc"):

        if len(state.messages) == 0:
            st3, st4 = st.columns(2)

            with st3:
                with st.chat_message("assistant"):
                    response_1 = st.write_stream(gr.introduction_response())

            state.messages.append(
                {
                    "role": "assistant",
                    "content": response_1
                }
            )

        # Add user message to chat history
        state.messages.append(
            {
                "role": "user",
                "content": prompt
             }
        )

        st5, st6 = st.columns(2)

        # Display user message in chat message container
        with st6:
            with st.chat_message("user"):
                st.markdown(prompt)

        st7, st8 = st.columns(2)

        # Add assistant response to chat history
        state.question += '|' + prompt

        try:
            target1 = gr.check_question(state.question.split('|')[-2])
        except:
            target1 = gr.check_question(state.prompt)

        target2 = gr.check_question(prompt)

        try:
            if target2 != 'Wrong':
                if target1 == target2:
                    forward_message = gr.generate_response(state.question)
                else:
                    forward_message = gr.generate_response(prompt)
                    state.question = ''
            else:
                forward_message = gr.wrong_response()
        except:
            forward_message = gr.wrong_response()
            state.question = "|".join(state.question.split("|")[:-1])

        # Display assistant response in chat message container
        with st7:
            with st.chat_message("assistant"):
                response_2 = st.write_stream(gr.stream_response(forward_message))

        # Add assistant response to chat history
        state.messages.append(
            {
                "role": "assistant",
                "content": response_2
            }
        )

else:
    st.error("Please sign-in on the menu login with the correct username and password")
