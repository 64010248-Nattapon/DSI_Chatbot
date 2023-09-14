import streamlit as st
from streamlit_chat import message
from utils import *
import streamlit as st
import streamlit_authenticator as stauth
from dependancies import sign_up, fetch_users
from main import chatbot


st.set_page_config(
        page_title="DSI AI Chatbot"
    )

def mainn():
    
    headerSection = st.container()

    def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://cdn.pic.in.th/file/picinth/backgroundRobot.jpeg");
                background-attachment: fixed;
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        ) 

    try:
        
        def show_login():
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

            email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

            info, info1 = st.columns(2)
            
            if not authentication_status:
                if st.button("สมัครสมาชิก", type="primary") :
                        st.session_state['loggedIn']=True
                        
            st.markdown(
            """
            <style>
            button[kind="primary"] {
                background: none!important;
                border: none;
                padding: 0!important;
                color: write !important;
                text-decoration: none;
                cursor: pointer;
                border: none !important;
            }
            button[kind="primary"]:hover {
                text-decoration: none;
                color: black !important;
            }
            # button[kind="primary"]:focus {
            #     outline: none !important;
            #     box-shadow: none !important;
            #     color: black !important;
            # }
            </style>
            """,
            unsafe_allow_html=True,
            )

            if username:
                if username in usernames:
                    if authentication_status:
                        st.session_state['loggedIn']=False
        
                        st.sidebar.subheader(f'ยินดีต้อนรับ {username}')
                        Authenticator.logout('ออกจากระบบ', 'sidebar')
                        if authentication_status==True:
                            chatbot()
                      
                        
                    elif not authentication_status:
                        with info:
                            st.error('รหัสผ่านหรือชื่อผู้ใช้ไม่ถูกต้อง')
                    else:
                        with info:
                            st.warning('โปรดป้อนข้อมูลประจำตัวของคุณ')
                else:
                    with info:
                        st.warning('ไม่มีชื่อผู้ใช้ กรุณาลงทะเบียน')
                        
        with headerSection:
            if 'loggedIn' not in st.session_state:
                st.session_state['loledIn'] =False
                show_login()
                add_bg_from_url()
            else:
                if st.session_state['loggedIn']:
                    sign_up()
                    add_bg_from_url()
                else:
                    show_login()
        
        
    except:
            st.success('Refresh Page')

if __name__ == '__main__':
    mainn()




# def set_background_image(image_url):
#     style = f"""
#     <style>
#     body {{
#         background-image: url("{image_url}");
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(style, unsafe_allow_html=True)

# # Call the function and pass the URL of the image you want to use as a background
# set_background_image("backgroundRobot.jpg")