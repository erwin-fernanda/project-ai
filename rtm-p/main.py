from streamlit_multipage import MultiPage
from tools import anomaly_detection as dt
from tools import processing_data as pdt
from tools import building_model as bd
from tools import check_email, update_json, replace_json, check_account
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def sign_up(st, **state):
    placeholder = st.empty()

    with placeholder.form("Sign Up"):
        image = Image.open("images/logo_rtm-p.png")
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
            image = Image.open("images/logo_rtm-p.png")
            st1, st2, st3 = st.columns(3)

            with st2:
                st.image(image)

            st.markdown("#### Login RTM-P app")
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


def dashboard(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Dashboard</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.write('What kind moving time do you want?')

        if st.checkbox('Days'):
            spacing = st.slider("How the spacing time in day do you want?", 1, 30, 1)
            spacing = spacing * 24
        elif st.checkbox('Hours'):
            spacing = st.slider("How the spacing time in hours do you want?", 1, 24, 1)
        else:
            spacing = 1

    with col2:
        st.write("Where the well and simulator do you want to monitor?")
        well = st.selectbox("Please choice one well!", ["L26E",
                                                        "L26F",
                                                        "L26G",
                                                        "L26H"])

        file_name = "data/dataset" + "_" + well + ".csv"
        data = pd.read_csv(file_name, sep=",")
        column_data = np.asarray(data.columns.values[1:])
        column_data = np.insert(column_data, 0, "All GG Temp")
        column_data = np.insert(column_data, 9, "GG Temp Avg")

        column = st.selectbox("Please choice one part simulator!", column_data)

    # Monitoring Plot

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Monitoring Well " + well + " Part " + column + "</h3>",
                unsafe_allow_html=True)

    data = pdt.create_data(data)
    # data.ewm(span=spacing).mean()

    data.dropna(inplace=True)

    if column == "All GG Temp":
        data_monitor = data.loc[:, ["TimeStamp",
                                    "GG Temp 1",
                                    "GG Temp 2",
                                    "GG Temp 3",
                                    "GG Temp 4",
                                    "GG Temp 5",
                                    "GG Temp 6",
                                    "GG Temp 7",
                                    "GG Temp 8"]]
        column = "GG Temp Avg"

    else:
        data_monitor = data.loc[:, ["TimeStamp",
                                    column]]

    column_monitor = data_monitor.columns

    col3, col4 = st.columns(2)

    with col3:
        low = float(st.number_input(str('Insert a lowest limit for safety (' + pdt.unit(column) + ")")))

    with col4:
        high = float(st.number_input(str('Insert a highest limit for safety (' + pdt.unit(column) + ")")))

    placeholder = st.empty()

    with st.spinner('Wait for it...'):
        time.sleep(5)

    colors = ["black",
              "blue",
              "yellow",
              "green",
              "brown",
              "grey",
              "red",
              "purple"]

    fig, ax = plt.subplots()
    j = 1
    maxim = len(data)

    while j <= maxim:
        with placeholder.container():
            for k in range(1, len(column_monitor)):
                ax.plot(range(0, j), data_monitor[column_monitor[k]].iloc[0:j], color=colors[k - 1])
                dataset = data.loc[0:j, ["TimeStamp",
                                         column]]

                value = dt.anomaly_detection_manual(dataset, column, high, low)

                for m in range(len(value)):
                    ax.axvspan(value[m] - 5, value[m] + 5, facecolor='0.5')

            ax.set_xlim(0, maxim)
            ax.set_ylim(min(data_monitor[column_monitor[1]]), max(data_monitor[column_monitor[1]]))
            ax.set_title(str(data["TimeStamp"].iloc[j]))
            ax.set_xlabel("Index")
            ax.set_ylabel(pdt.unit(column))
            ax.legend(column_monitor[1:], loc=4, fontsize='xx-small')

            st.pyplot(fig)

            if len(value) > 0:
                st.write("Anomaly Detection Log Information")
                st.table(dataset.iloc[value])

            j += spacing

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


def insight(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Data Insight</h3>", unsafe_allow_html=True)

    st.write("Where the well do you want to get more information?")
    well = st.selectbox("Please choice one!", ["L26E",
                                               "L26F",
                                               "L26G",
                                               "L26H"])
    file_name = "data/dataset" + "_" + well + ".csv"
    data = pd.read_csv(file_name, sep=",")
    column_data = np.asarray(data.columns.values[1:])
    column_data = np.insert(column_data, 8, "GG Temp Avg")

    column = st.selectbox("Please choice one part simulator!", column_data)

    # Monitoring Plot

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Graph Insight Well " + well + " Part " + column + "</h3>",
                unsafe_allow_html=True)

    data = pdt.create_data(data)
    # data.ewm(span=spacing).mean()

    data.dropna(inplace=True)

    dataset = data.loc[:, ["TimeStamp",
                           column]]
    dataset["TimeStamp"] = pd.to_datetime(dataset['TimeStamp'])
    dataset["Year"] = dataset['TimeStamp'].dt.year
    dataset["Quarter"] = dataset['TimeStamp'].dt.quarter
    dataset["Month"] = dataset['TimeStamp'].dt.month
    dataset["Day"] = dataset['TimeStamp'].dt.day
    dataset["Hours"] = dataset['TimeStamp'].dt.hour
    dataset["Minutes"] = dataset['TimeStamp'].dt.minute

    data_year = dataset.groupby('Year')
    data_quarter = dataset.groupby('Quarter')
    data_month = dataset.groupby('Month')
    data_day = dataset.groupby('Day')

    with st.spinner('Wait for it...'):
        time.sleep(5)

    figs = plt.figure(figsize=(15, 5))
    data_year[column].agg('mean').plot()
    plt.xlabel("Year")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Year'))
    st.pyplot(figs)

    figs = plt.figure(figsize=(15, 5))
    data_quarter[column].agg('mean').plot()
    plt.xlabel("Quarter")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Quarter'))
    st.pyplot(figs)

    figs = plt.figure(figsize=(15, 5))
    data_month[column].agg('mean').plot()
    plt.xlabel("Month")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Month'))
    st.pyplot(figs)

    figs = plt.figure(figsize=(15, 5))
    data_day[column].agg('mean').plot()
    plt.xlabel("Days")
    plt.ylabel(pdt.unit(column))
    plt.title(str('Data Insight ' + column + ' by Day'))
    st.pyplot(figs)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)


def deployment(st, **state):
    # Title
    global history, model, fig
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Deployment Model</h3>", unsafe_allow_html=True)

    well = st.selectbox("Please choice the well!", ["L26E",
                                                    "L26F",
                                                    "L26G",
                                                    "L26H"])
    file_name = "data/dataset" + "_" + well + ".csv"
    data = pd.read_csv(file_name, sep=",")
    data = pdt.create_data(data)
    # data.ewm(span=spacing).mean()

    data.dropna(inplace=True)

    # st.dataframe(data)

    column_feature = data.columns.values[1:]

    feature = st.selectbox("Please choice one column as feature anomaly detection!", column_feature)

    col5, col6 = st.columns(2)

    with col5:
        low = float(st.number_input(str('Insert a lowest limit for safety (' + pdt.unit(feature) + ")")))

    with col6:
        high = float(st.number_input(str('Insert a highest limit for safety (' + pdt.unit(feature) + ")")))

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Building Model</h3>", unsafe_allow_html=True)

    with st.spinner('Wait for it...'):
        time.sleep(5)

    try:
        data_ml = dt.anomaly_detection(data, high, low, feature)

        kind_ml = st.selectbox("Please select your kind model!", ["Supervised Learning",
                                                                  "Unsupervised Learning"])

        if kind_ml == "Supervised Learning":
            model = ["Logistic Regression",
                     "Random Forest",
                     "SVM"]

        elif kind_ml == "Unsupervised Learning":
            model = ["LSTM",
                     "CNN"]

        model_ml = st.radio("Please select model deep learning do you want!", model)

        train_size = float(st.number_input('Please input train size do you want! (value: 0 - 1)'))

        st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                    "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
        st.markdown("<h3 style=\"text-align:center;\">Accuracy Model</h3>", unsafe_allow_html=True)

        try:
            if model_ml == "LSTM":
                model, fig = bd.model_lstm(data, data_ml, train_size)
            elif model_ml == "CNN":
                model, fig = bd.model_cnn(data, data_ml, train_size)
            elif model_ml == "Logistic Regression":
                model, fig = bd.model_logistic(data, data_ml, train_size)
            elif model_ml == "Random Forest":
                model, fig = bd.model_random_forest(data, data_ml, train_size)
            elif model_ml == "SVM":
                model, fig = bd.model_svm(data, data_ml, train_size)

            st.pyplot(fig)

        except:
            st.error("Please input train size your model!")

    except:
        st.error("Please input the value of highest and lowest limit safety!")


def messages(st, **state):
    # Title
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    restriction = state["login"]

    if "login" not in state or restriction == "False":
        st.warning("Please login with your registered email!")
        return

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Messages</h3>", unsafe_allow_html=True)

    placeholder = st.empty()

    with placeholder.form("Message"):
        email = st.text_input("Email")
        text = st.text_area("Messages")
        submit = st.form_submit_button("Send")

    if submit and check_email(email) == "valid email":
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
    image = Image.open("images/logo_rtm-p.png")
    st1, st2, st3 = st.columns(3)

    with st2:
        st.image(image)

    st.markdown("<svg width=\"705\" height=\"5\"><line x1=\"0\" y1=\"2.5\" x2=\"705\" y2=\"2.5\" stroke=\"black\" "
                "stroke-width=\"4\" fill=\"black\" /></svg>", unsafe_allow_html=True)
    st.markdown("<h3 style=\"text-align:center;\">Account Setting</h3>", unsafe_allow_html=True)

    restriction = state["login"]
    password = state["password"]

    if "login" not in state or restriction == "False":
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
app.add_app("Dashboard", dashboard)
app.add_app("Data Insight", insight)
app.add_app("Deployment Model", deployment)
app.add_app("Messages", messages)
app.add_app("Account Setting", account)
app.add_app("Logout", logout)

app.run()
