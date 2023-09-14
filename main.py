from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *

def chatbot():
    st.subheader("DSI AI Chatbot")
        
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["คุณสามารถถามข้อกฎหมาย, ร้องเรียนDSI และกรอกแบบฟอร์มยื่นDSI ได้ ผ่านฉัน"]

    if 'requests' not in st.session_state:
        st.session_state['requests'] = []

    llm = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key="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")

    if 'buffer_memory' not in st.session_state:
                st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


    system_msg_template = SystemMessagePromptTemplate.from_template(template="""ตอบคำถามตามความเป็นจริงมากที่สุดโดยใช้ข้อมูลจากฐานข้อมูลเวกเตอร์และข้อความด้านล่าง ถ้าไม่มีคำตอบใดๆเลย ตอบว่า 'ขออภัยไม่สามารถตอบคำถามนี้ได้',ถามเกี่ยวกับในประโยคนี้ แจ้งเบาะแส ร้องเรียน ร้องทุกข์หรือแจ้งออนไลน์ 'คุณสามารถแจ้งเบาะแส ร้องเรียน ร้องทุกข์หรือแจ้งออนไลน์ \n https://register.dsi.go.th/',
    ถามเกี่ยวกับในประโยคนี้ ร้องเรียนการทุจริตและประพฤติมิชอบของเจ้าหน้าที่กรมสอบสวนคดีพิเศษ  ตอบ 'คุณสามารถร้องเรียนการทุจริตและประพฤติมิชอบของเจ้าหน้าที่กรมสอบสวนคดีพิเศษ ผ่านลิงค์ \nhttps://docs.google.com/forms/d/e/1FAIpQLSe78jsewoR52J-cz9JSCbBtI_Mv-HaxEEx73_yFxIC2HPn5IQ/viewform?fbzx=3652361012213309990',
    ถามเกี่ยวกับในประโยคนี้ว่า ร้องเรียนการจัดซื้อจัดจ้าง ตอบ 'สามารถร้องเรียน ร้องทุข์ : \nhttps://register.dsi.go.th/',
    ตรวจสอบสถานะร้องเรียน ตอบ 'สามารถตรวจสอบสถานะร้องเรียน \nhttps://register.dsi.go.th/status',ถ้าถามเกี่ยวกับประโยคนี้ พระราชบัญญัติที่อ้างอิงนี้คือ ตอบ 'พระราชบัญญัติ ว่าด้วยการกระทําความผิดเกี่ยวกับคอมพิวเตอร์ (ฉบับที่ ๒)   พ.ศ. ๒๕๖๐ สมเด็จพระเจ้าอยู่หัวมหาวชิราลงกรณ บดินทรเทพยวรางกูร ให้ไว้ ณ วันที่ ๒๓ มกราคม พ.ศ. ๒๕๖๐ เป็นปีที่ ๒ ในรัชกาลปัจจุบัน  และปี 2550''""")


    human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

    prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)


    # container for chat history
    response_container = st.container()
    # container for text box
    textcontainer = st.container()
    
    with textcontainer:
        query = st.text_input("สอบถาม ", key="input")
        if query:
            with st.spinner("กำลังคิด..."):
                conversation_string = get_conversation_string()
                # st.code(conversation_string)                        
                refined_query = query_refiner(conversation_string, query)
                # st.subheader("ข้อความค้นหาละเอียด")
                # st.write(refined_query)
                context = find_match(refined_query)
                # print(context)  
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
            st.session_state.requests.append(query)
            st.session_state.responses.append(response) 
            
    with response_container:
        if st.session_state['responses']:

            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i))
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

chatbot()
            