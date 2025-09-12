
import streamlit as st
from streamlit import session_state  # session_state dictionary user inputs aur app state ko memory mein store karta hai

import uuid  # unique thread ID generate karne ke liye library
import time
# chatbot backend functionalities import kar rahe hain
from backend_Langgraph_Database import *

# ************************ Utility Functions *******************************************

# Unique thread ID generate karne ke liye function
def generate_uuid_thread():
    thread_id = uuid.uuid4()  # random unique ID create karega
    return thread_id

# Chat reset karne ke liye function – jab user "New Chat" button dabaye
def reset_chat():
    thread_id = generate_uuid_thread()  # naya unique thread ID generate karein
    st.session_state['thread_id'] = thread_id  # session state mein naye thread ID ko store karein
    st.session_state['current_thread'] = thread_id  # current active thread bhi update karo
    add_threads(thread_id)  # naye thread ko thread list mein add karein
    st.session_state['message_history'] = []  # chat history ko clear kar dein

# Agar thread list mein thread_id nahi hai to use add karein
def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# Diye gaye thread ID ke liye saved conversation load karne ka function
def load_conversation(thread_id):
    result = workflow.get_state(config={"configurable": {'thread_id': thread_id}})
    if result and result.values and 'message' in result.values:
        return result.values['message']
    return []

# ************************ Session Initialization ****************************************

# Agar message history session state mein nahi hai to initialize karo
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

# Agar thread ID session state mein nahi hai to generate karo
if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generate_uuid_thread()

# Agar current_thread session state mein nahi hai to initialize karo
if "current_thread" not in st.session_state:
    st.session_state['current_thread'] = st.session_state['thread_id']

# Agar chat_threads session state mein nahi hai to initialize karo
if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_unique_thread()

# Current thread ko thread list mein add karo agar already nahi hai
add_threads(st.session_state['thread_id'])

# ************************ Sidebar Setup ************************************************

# Sidebar ka title
st.sidebar.title("New Conversation")

# 'New Chat' button – click karne par naye thread ke saath conversation reset hogi
if st.sidebar.button("New Chat"):
    reset_chat()

# Sidebar mein "My Conversations" heading
st.sidebar.header("Chat History")

# Sidebar mein saved threads dikhana – har thread ka button
for thread_id in st.session_state['chat_threads'][::-1]:  # latest thread upar dikhayein
    if st.sidebar.button(str(thread_id), key=str(thread_id)):  # unique key se buttons ko alag pehchano
        # jab user kisi thread par click kare
        st.session_state['thread_id'] = thread_id
        st.session_state['current_thread'] = thread_id
        msg = load_conversation(thread_id)
        
        # saved messages ko UI compatible format mein convert karo
        temp_msg = []
        for message in msg:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "AI"
            temp_msg.append({'role': role, 'content': message.content})
        
        # message history update karo
        st.session_state['message_history'] = temp_msg

# ************************ Sync Messages if Thread Changed ********************************

# agar thread_id aur current_thread match nahi karte to conversation reload karo
if st.session_state.get('current_thread') != st.session_state.get('thread_id'):
    msg = load_conversation(st.session_state['thread_id'])
    temp_msg = []
    for message in msg:
        if isinstance(message, HumanMessage):
            role = "user"
        else:
            role = "AI"
        temp_msg.append({'role': role, 'content': message.content})
    st.session_state['message_history'] = temp_msg
    st.session_state['current_thread'] = st.session_state['thread_id']

# ************************ Display Chat Messages ************************************

# har message ko loop karke UI mein dikhana
for message in st.session_state['message_history']:
    with st.chat_message(name=message['role']):
        st.text(message['content'])

# ************************ Taking Input from User ************************************

# chat input box jahan user apna message type karega
user_input = st.chat_input("Type Here")

# agar user ne input diya hai to process karo
if user_input:
    try:
        # user ka message session state mein add karo
        st.session_state['message_history'].append({"role": "user", "content": user_input})
        
        # user ka message UI mein dikhana
        with st.chat_message(name="user"):
            st.write(user_input)
        
        
        
        
        
        # typing effect ko simulate karne ke liye function
        def typing_effect(user_input, thread_id):
            # AI ke liye initial state prepare karna
            initial_state = ChatbotState(message=[HumanMessage(content=user_input)])
            config1 = {
                'configurable': {'thread_id': thread_id},
                #using thread_id grouping all messages showing them in langsmith with turn msg form mei.
                "metadata":{'thread_id': thread_id}, 
                "run_name":'chat_turn'
                
                }
            
            # workflow invoke karke AI ka response lena
            response = workflow.invoke(input=initial_state, config=config1)
            ai_response = response['message'][-1].content
            
            # AI ka response session state mein add karna
            st.session_state['message_history'].append({"role": "AI", "content": ai_response})
            
            # AI ka response word by word dikhana
            for word in ai_response.split():
                yield word + " "
                time.sleep(0.05)  # 50ms ka delay, chaaho to badal sakte ho
        
        # AI ka message UI mein dikhana
        with st.chat_message(name="AI"):
            st.write_stream(typing_effect(user_input=user_input, thread_id=st.session_state['thread_id']))
            
    except Exception as e:
        print("Error:", e)