import os
import requests
import streamlit as st
from streamlit_chat import message


def home_page():
    st.header("Open Domain Question Answering Chatbot")

    st.markdown("""
                Hi there 👋, welcome to open domain QA chatbot!. Here, you can get answers of your general queries.

                **Features**:
                * Uses Wikipedia and Google as the knowledge base
                * Uses advanced NLP techniques to get correct answers of queries with confidence score    
            """)
    st.write(st.session_state)
def chatbot_page():
    st.header("Open Domain Question Answering Chatbot")
    with st.form("Question", clear_on_submit=True):
        prompt= st.text_input("Ask your question here..")
        submit_btn = st.form_submit_button()

    col1, col2 = st.columns(2)
    with col1:
        kb_selected = st.radio(label="Select the knowledge base: ", options=("Wikipedia", "Google"), horizontal=True)
    
    with col2:
        clear_chat_btn = st.button("Clear Chat")
        st.session_state['clear_chat_flag'] = clear_chat_btn

    st.session_state['kb']=kb_selected
    st.session_state['clear_chat_flag'] = clear_chat_btn

    if "messages" not in st.session_state:
        st.session_state['messages']=[{"role":"assistant", "content":"Hi there 👋, ask me any general question.."}]
    
    if st.session_state['clear_chat_flag']:
        st.session_state['messages']=[]

    for msg in st.session_state['messages']:
        message(message=msg['content'], is_user=True if msg['role']=="user" else False)

    if len(prompt)>0 and submit_btn:
        st.session_state['messages'].append({"role":"user", "content":prompt})
        message(message=prompt, is_user=True)
        try:
            if st.session_state['kb']=="Wikipedia":
                url = "http://localhost:5000/get_wiki_answer"
                response = requests.post(url=url, json={"question":prompt}).json()
                output = f"Answer: {response[0]['answer']}, Confidence Score:{str(round(response[0]['score'],2))}"
                print(output)
                message(message=output, is_user=False)
            elif st.session_state['kb']=="Google":
                url = "http://localhost:5000/get_google_answer"
                response = requests.post(url=url, json={"question":prompt}).json()
                output = f"Answer: {response[0]['answer']}, Confidence Score:{str(round(response[0]['score'],2))}"
                print(output)
                message(message=output, is_user=False)

        except:
             output = "Some error occured..Pls try again"
             message(message=output, is_user=False)   
        
        st.session_state['messages'].append({"role":"assistant", "content":output})        

def main():
    st.set_page_config(page_title="Open Domain Question Answering Chatbot", layout="wide")
    if 'page' not in st.session_state:
        st.session_state['page']='home'
    
    st.sidebar.title("Navigation")

    page = st.sidebar.radio(label="Go to", options=("home", "chatbot"))

    if page=="home":
        home_page()
    elif page=="chatbot":
        chatbot_page()


if __name__=='__main__':
    main()

