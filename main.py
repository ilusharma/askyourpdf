import streamlit as st
import pandas as pd
from chatbot import create_user, create_chat_id, check_usage, create_conversation, init_chat, file_upload,chatBot
from streamlit_javascript import st_javascript
import json


st.set_page_config(page_title="Home Page", page_icon=":bar_chart:", layout="wide")
st.title("Ask from PDF")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



def get_from_local_storage(k):
    v = st_javascript(
        f"JSON.parse(localStorage.getItem('{k}'));"
    )
    return v or {}


def set_to_local_storage(k, v):
    jdata = json.dumps(v)
    st_javascript(
        f"localStorage.setItem('{k}', JSON.stringify({jdata}));"
    )


user_id = get_from_local_storage('user_id')
st.session_state.user_id = user_id
chat_id = get_from_local_storage('chat_id')
st.session_state.chat_id = chat_id

if st.session_state.user_id == {}:
    user_id = create_user()
    chat_id = create_chat_id(user_id)
    st.session_state.chat_id = chat_id
    set_to_local_storage('chat_id', chat_id)
    st.session_state.user_id = user_id
    set_to_local_storage('user_id', user_id)

docID = get_from_local_storage('docId')
st.session_state.docId = docID



#session for user id
#create button to create user id

#create 3 buttons in one row
recreate_user_id,userid_detail = st.columns(2)
recreate_userID = recreate_user_id.button("Recreate User ID")
usage,usage_detail = st.columns(2)
st.write("User ID: ", st.session_state.user_id)

# usage = usage.button("Usage")
#
if recreate_userID:
    user = create_user()
    chat_id = create_chat_id(user)
    st.session_state.chat_id = chat_id
    set_to_local_storage('chat_id', chat_id)
    st.session_state.user_id = user
    set_to_local_storage('user_id', user)




#
# if usage:
#     usage = check_usage(st.session_state.user_id)
#     usage = json.loads(usage)
#     usage_detail.dataframe(usage)


#upload file
file = st.file_uploader("Upload file", type=['pdf'])
if file is not None:
    file_details = {"FileName":file.name,"FileType":file.type,"FileSize":file.size}
    data = file_upload(st.session_state.user_id,file)

    st.session_state.docId = data
    set_to_local_storage('docId', data)
    st.write('File uploaded successfully and docId is: ', st.session_state.docId)

    #init chat
    init_chat(st.session_state.user_id, st.session_state.chat_id)
    print("init chat")


    conversation = create_conversation(st.session_state.user_id)
    print(conversation)


    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # React to user input
    if prompt := st.chat_input(""):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        #add loader

        print('i am before chat bot')

        chat_message = chatBot(st.session_state.user_id, st.session_state.docId, st.session_state.chat_id, prompt)
        print('i am after chat bot')
        response = f"{chat_message}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})





