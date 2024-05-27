from PIL import Image
import streamlit as st
from streamlit import session_state as state

st.set_page_config(
    page_title="Turbo-Doc App",
    page_icon="💬",
)

image = Image.open(f'./image/turbodoc_logo.png')

sta, stb, stc = st.columns(3)

with stb:
    st.image(image)

# st.markdown('<h3 style="text-align: center;">Turbo-Doc Application</h3>', unsafe_allow_html=True)

placeholder = st.empty()

with placeholder.form(key='Login'):
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submit = st.form_submit_button(
        'Login',
        use_container_width=True
    )

    st.write("Have you registered account in this app before? "
             "If you haven't yet, please contact the Turbodoc admin!")

    state['username'] = username
    state['password'] = password
    state['login'] = submit

if submit:
    username_ori = st.secrets[state['username']]['username']
    password_ori = st.secrets[state['username']]['password']

else:
    username_ori = ''
    password_ori = ''
    state['username'] = None
    state['password'] = None


# Main Application

if state['login'] and (username_ori == state['username'] and password_ori == state['password']):
    placeholder.empty()
    st.success('Login successfully')

elif state['login'] and (username_ori != username or password_ori != password):
    st.error("You haven't registered to the Turbodoc app! Please contact Turbodoc admin!")

else:
    st.error("Please input username and password!")

