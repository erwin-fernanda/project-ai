import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit UI
st.title("Email Sender")

# Email credentials and settings
st.sidebar.header("Email Settings")
email = st.sidebar.text_input("Your Email")
password = st.sidebar.text_input("Your Email Password", type="password")
recipient = st.sidebar.text_input("Recipient Email")
subject = st.sidebar.text_input("Subject")
message = st.sidebar.text_area("Message")


# Email sending function
def send_email():
    try:
        # Establishing connection with SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)

        # Constructing the email
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = recipient
        msg["Subject"] = subject
        body = message
        msg.attach(MIMEText(body, "plain"))

        # Sending the email
        server.sendmail(email, recipient, msg.as_string())
        st.success("Email sent successfully!")

        # Closing the server connection
        server.quit()
    except Exception as e:
        st.error(f"Error: {e}")


# Send button
if st.sidebar.button("Send Email"):
    if email and password and recipient and subject and message:
        send_email()
    else:
        st.warning("Please fill in all fields.")