from PIL import Image
import streamlit as st
from streamlit import session_state as state


if 'login' not in list(state.keys()):
    state['login'] = False


def clear_cache():
    keys = list(state.keys())
    for key in keys:
        state.pop(key)


# st.button('Clear Cache', on_click=clear_cache)

image = Image.open(f'./image/turbodoc_logo.png')

sta, stb, stc = st.columns(3)

with stb:
    st.image(image)

# st.markdown('<h3 style="text-align: center;">Turbo-Doc Application</h3>', unsafe_allow_html=True)

if state['login']:
    placeholder = st.empty()

    with placeholder.form(key='Login'):
        submit = st.form_submit_button(
            'Logout',
            use_container_width=True
        )

        st.write("Are you sure to logout the Turbodoc?")

    if submit:
        clear_cache()
        st.success("Thanks for using Turbodoc. You have logout successfully")
        # placeholder = st.empty()
else:
    st.error("Please sign-in on the Login Menu with the correct username and password")