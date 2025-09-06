import streamlit as st
from streamlit import session_state  # this class will be dict object 
# whenever user provide input from UI page session_state ke inside information remain there.
from backend_UI import workflow,HumanMessage,AIMessage


# now checking if message_history of list in session state of Dictatonary or not
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

# now loading the conversational history.
for message in st.session_state['message_history']:   # ✅ corrected key name
    # now setting the user input to chatmessage component mei.
    with st.chat_message(name=message['role']):
        st.text(message['content'])  # ✅ corrected, no "body" argument in st.text()
        

# defining chat_input box.
user_input = st.chat_input(placeholder="Type Here")

# now setting the user input to chatmessage component mei.
if user_input:
    # now appending the chat history to session_state
    st.session_state['message_history'].append({'role': "user", 'content': user_input})
    with st.chat_message(name="user"):
        st.text(user_input)
        
    #before invoking the chatbot workflow. we have to define configuration
    config = {'configurable': {'thread_id':"1"}}
        
        
    #now invoking the worklfow of chatbot.
    ai_response = workflow.invoke({'message':HumanMessage(content=user_input)},config=config)
    
    #fetching last AI message
    ai_msg = ai_response['message'][-1].content
    

    
    # now appending the chat history to session_state
    st.session_state['message_history'].append({'role': "AI", 'content': ai_msg})
    
    # now setting the AI response to chatmessage component mei.
    with st.chat_message(name="AI"):
        st.text(ai_msg)  # ✅ show proper AI response
