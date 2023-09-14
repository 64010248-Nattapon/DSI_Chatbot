
import streamlit as st
from streamlit_chat import message
from utils import *

import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users


st.set_page_config(page_title='testWebDSI', initial_sidebar_state='collapsed')

# st.markdown(
#     """
#     <style>
#     .login-button {
#         display: inline-block;
#         background-color: green;
#         color: white;
#         padding: 10px 20px;
#         border-radius: 5px;
#         border: none;
#         cursor: pointer;
#         text-align: center;
#         text-decoration: none;
#         font-size: 16px;
#     }
#     </style>
#     """
# )

try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)
    

# # สร้างปุ่ม login
#     if st.button("Login", key="login_button"):
    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')
    info, info1 = st.columns(2)

    if not authentication_status:
        sign_up()

    if username:
        if username in usernames:
            print("username:",username)
            print("usernames:",usernames)
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.subheader('หน้า chatbot')
                st.markdown(
                    """ Chatbot """
                )

            elif not authentication_status:
                with info:
                    st.error('รหัสผ่านหรือชื่อผู้ใช้ไม่ถูกต้อง')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')


except:
    st.success('กรุณา Refresh Page')