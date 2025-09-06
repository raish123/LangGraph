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
        
    
    
    config1 = {"configurable": {'thread_id':'1'}}
    
    # now setting the AI response to chatmessage component mei.
    with st.chat_message(name="AI"):
        
        #write_stream method --- Iska use tab hota hai jab aapko LLM ka response stream karke dikhana ho
        ai_response_typing = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in workflow.stream(
                input={"message": HumanMessage(content=user_input)},
                config=config1,
                stream_mode="messages"
            )
        )

        
    # now appending the chat history to session_state
    if ai_response_typing.strip():
        st.session_state['message_history'].append({'role': "AI", 'content': ai_response_typing})