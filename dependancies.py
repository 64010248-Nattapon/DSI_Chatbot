import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta

DETA_KEY = 'c0jzdemxyuq_Gfrd7tkgV7X4qJPRZnQF2bDDh2oEwtiU'
deta = Deta(DETA_KEY)
db= deta.Base('Datawebdsi')

def insert_user(email, username,password):
    """
    Inserts Users into the DB
    :param email:
    :param username:
    :param password:
    :return User Upon successful Creation:
    """
    date_joined = str(datetime.datetime.now())

    return db.put({'key': email, 'username': username, 'password': password, 'date_joined': date_joined})

# insert_user('nuttest@gmail.com','test','12345678')


def fetch_users():
    """
    Fetch Users
    :return Dictionary of Users:
    """
    users = db.fetch()
    return users.items


def get_user_emails():
    """
    Fetch User Emails
    :return List of user emails:
    """
    users = db.fetch()
    emails = []
    for user in users.items:
        emails.append(user['key'])
    return emails


def get_usernames():
    """
    Fetch Usernames
    :return List of user usernames:
    """
    users = db.fetch()
    usernames = []
    for user in users.items:
        usernames.append(user['key'])
    return usernames

def validate_email(email):
    """
    Check Email Validity
    :param email:
    :return True if email is valid else False:
    """
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern, email):
        return True
    return False


def validate_username(username):
    """
    Checks Validity of userName
    :param username:
    :return True if username is valid else False:
    """

    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, username):
        return True
    return False

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False

def sign_up():
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':white[สมัครสมาชิก]')
        email=st.text_input('อีเมล', placeholder='กรุณาใส่ อีเมล') #เปลี่ยนสี ตัวหนังสือ:color[Email]
        username=st.text_input('ชื่อผู้ใช้',placeholder='กรุณาใส่ ชื่อผู้ใช้')
        password1=st.text_input('รหัสผ่าน', placeholder='กรุณาใส่ รหัสผ่าน',type='password')
        password2=st.text_input('ยืนยัน รหัสผ่าน', placeholder='ยืนยัน รหัสผ่าน', type='password')
        
        if email:
            if validate_email(email):
                if email not in get_user_emails():
                    if validate_username(username):
                        if username not in get_usernames():
                            if len(username) >= 2:
                                if len(password1) >= 6:
                                    if password1 == password2:
                                        # Add User to DB
                                        hashed_password = stauth.Hasher([password2]).generate()
                                        insert_user(email, username, hashed_password[0])
                                        st.success('สร้างบัญชีเสร็จสิ้น!!')
                                        # st.balloons() #แอฟเฟค
                                    else:
                                        st.warning('รหัสผ่านไม่ตรงกัน')
                                else:
                                    st.warning('รหัสผ่านสั้นเกินไป')
                            else:
                                st.warning('ชื่อผู้ใช้สั้นเกินไป')
                        else:
                            st.warning('มีชื่อผู้ใช้อยู่แล้ว')

                    else:
                        st.warning('ชื่อผู้ใช้ไม่ถูกต้อง')
                else:
                    st.warning('มีอีเมลนี้อยู๋แล้ว!!')
            else:
                st.warning('อีเมลไม่ถูกต้อง')

        btn1, bt2, btn3, btn4, btn5 = st.columns(5)

        with btn3:
            st.form_submit_button('สมัครสมาชิก')
            
# sign_up()