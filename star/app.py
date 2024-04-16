import os

from streamlit_multipage import MultiPage
from utils import check_email, check_account, update_json, replace_json, change_path_band
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")


def sign_up(st, **state):
    placeholder = st.empty()

    with placeholder.form("Sign Up"):
        image = Image.open("images/logo_star.png")
        st1, st2, st3 = st.columns(3)

        with st2:
            st.image(image)

        st.warning("Please sign up your account!")

        # name_ = state["name"] if "name" in state else ""
        name = st.text_input("Name: ")

        # username_ = state["username"] if "username" in state else ""
        username = st.text_input("Username: ")

        # email_ = state["email"] if "email" in state else ""
        email = st.text_input("Email")

        # password_ = state["password"] if "password" in state else ""
        password = st.text_input("Password", type="password")

        save = st.form_submit_button("Save")

    if save and check_email(email) == "valid email":
        placeholder.empty()
        st.success("Hello " + name + ", your profile has been save successfully")
        MultiPage.save({"name": name,
                        "username": username,
                        "email": email,
                        "password": password,
                        "login": "True",
                        "edit": True})

        update_json(name, username, email, password)

    elif save and check_email(email) == "duplicate email":
        st.success("Hello " + name + ", your profile hasn't been save successfully because your email same with other!")

    elif save and check_email(email) == "invalid email":
        st.success("Hello " + name + ", your profile hasn't been save successfully because your email invalid!")

    else:
        pass


def login(st, **state):
    st.snow()
    # Create an empty container
    placeholder = st.empty()

    try:
        # Insert a form in the container
        with placeholder.form("login"):
            image = Image.open("images/logo_star.png")
            st1, st2, st3 = st.columns(3)

            with st2:
                st.image(image)

            st.markdown("#### Login STAR Website")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")

            st.write("Are you ready registered account in this app? If you don't yet, please sign up your account!")

            name, username, status = check_account(email, password)

        if submit and status == 'register':
            # If the form is submitted and the email and password are correct,
            # clear the form/container and display a success message
            placeholder.empty()
            st.success("Login successful")
            MultiPage.save({"name": name,
                            "username": username,
                            "email": email,
                            "password": password,
                            "login": "True"})

        elif submit and status == 'wrong password':
            st.error("Login failed because your password is wrong!")

        elif submit and status == 'not register':
            st.error("You haven't registered to this app! Please sign up your account!")

        else:
            pass

    except:
        st.error("Please login with your registered email!")


def input_data(st, **state):
    # Title
    image = Image.open("images/logo_star.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Input Data</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    uploaded_files = st.file_uploader("Please select your data do you want!",
                                      accept_multiple_files=True)

    for uploaded_file in uploaded_files:
        st.success("Your data " + uploaded_file.name + " has been successfully!")


def visualization_data(st, **state):
    # Title
    image = Image.open("images/logo_star.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Visualization Data</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    path = "data/lst/LC09_L1TP_124064_20220925_20220925_02_T1"
    path_file = []

    for paths in os.listdir(path):
        path_file.append(path + "/" + paths)

    band = change_path_band(path_file)

    kind_of_band = st.selectbox('Please select band do you want!',
                                band.keys())

    fig, ax = plt.subplots(1, figsize=(12, 10))
    src = rasterio.open(band[kind_of_band])
    ax.imshow(src.read(1))

    st.pyplot(fig)


def processing_data(st, **state):
    # Title
    image = Image.open("images/logo_star.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Processing Data</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    method = st.selectbox('Please select your method do you want!',
                          ['LST',
                           'NDWI',
                           'NDVI',
                           'SWIR'])

    result = "data/lst/map_lst.png"

    image = Image.open(result)

    st.image(image, caption=str('Map ' + method))


def report(st, **state):
    # Title
    image = Image.open("images/logo_star.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Messages Report</h3>", unsafe_allow_html=True)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    placeholder = st.empty()

    with placeholder.form("Message"):
        email = st.text_input("Email")
        text = st.text_area("Messages")
        submit = st.form_submit_button("Send")

    if submit and check_email(email) == "valid email" or check_email(email) == "duplicate email":
        placeholder.empty()
        st.success("Before your message will be send, please confirm your messages again!")
        vals = st.write("<form action= 'https://formspree.io/f/xeqdqdon' "
                        "method='POST'>"
                        "<label> Email: <br> <input type='email' name='email' value='" + str(email) +
                        "'style='width:705px; height:50px;'></label>"
                        "<br> <br>"
                        "<label> Message: <br> <textarea name='Messages' value='" + str(text) +
                        "'style='width:705px; height:200px;'></textarea></label>"
                        "<br> <br>"
                        "<button type='submit'>Confirm</button>"
                        "</form>", unsafe_allow_html=True)

        if vals is not None:
            st.success("Your messages has been send successfully!")

    elif submit and check_email(email) == "invalid email":
        st.success("Your message hasn't been send successfully because email receiver not in list")

    else:
        pass


def account(st, **state):
    # Title
    image = Image.open("images/logo_star.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Account Setting</h3>", unsafe_allow_html=True)

    restriction = state["login"]
    password = state["password"]

    if ("login" not in state or restriction == "False") or ("password" not in state):
        st.warning("Please login with your registered email!")
        return

    placeholder = st.empty()

    st.write("Do you want to edit your account?")
    edited = st.button("Edit")
    state["edit"] = np.invert(edited)

    old_email = state['email']

    with placeholder.form("Account"):
        name_ = state["name"] if "name" in state else ""
        name = st.text_input("Name", placeholder=name_, disabled=state["edit"])

        username_ = state["username"] if "username" in state else ""
        username = st.text_input("Username", placeholder=username_, disabled=state["edit"])

        email_ = state["email"] if "email" in state else ""
        email = st.text_input("Email", placeholder=email_, disabled=state["edit"])

        if edited:
            current_password = st.text_input("Old Password", type="password", disabled=state["edit"])
        else:
            current_password = password

        # current_password_ = state["password"] if "password" in state else ""
        new_password = st.text_input("New Password", type="password", disabled=state["edit"])

        save = st.form_submit_button("Save")

    if save and current_password == password:
        st.success("Hi " + name + ", your profile has been update successfully")
        MultiPage.save({"name": name,
                        "username": username,
                        "email": email,
                        "password": new_password,
                        "edit": True})

        replace_json(name, username, old_email, email, new_password)

    elif save and current_password != password:
        st.success("Hi " + name + ", your profile hasn't been update successfully because your current password"
                                  " doesn't match!")

    elif save and check_email(email) == "invalid email":
        st.success("Hi " + name + ", your profile hasn't been update successfully because your email invalid!")

    else:
        pass


def logout(st, **state):
    st.success("Your account has been log out from this app")
    MultiPage.save({"login": "False"})


app = MultiPage()
app.st = st

app.navbar_name = "Menu"
app.navbar_style = "VerticalButton"

app.hide_menu = False
app.hide_navigation = True

app.add_app("Sign Up", sign_up)
app.add_app("Login", login)
app.add_app("Input Data", input_data)
app.add_app("Visualization Data", visualization_data)
app.add_app('Processing Data', processing_data)
app.add_app("Report", report)
app.add_app("Account Setting", account)
app.add_app("Logout", logout)

app.run()
