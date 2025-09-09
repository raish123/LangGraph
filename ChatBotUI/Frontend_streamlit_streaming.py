import streamlit as st
from streamlit import session_state  # this class will be dict object 
# whenever user provide input from UI page session_state ke inside information remain there.
from backend_UI import workflow,HumanMessage,AIMessage,ChatbotState


# Agar 'chat_history' session state me nahi hai, to ise initialize karo
# Yeh list UI par ho rahi Human aur AI ki conversations ko store karegi below example manner mei as dictatonary
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []
    
# Example in session state how result will be store.
# st.session_state['message_history'] = [
#     {"role": "user/assistant", "content": "Hi AI, how are you?"},



# Below Code:
# UI par chat history dikhane ke liye likha gaya hai.
# Agar 'chat_history' session state me maujood hai, to usse iterate karke messages display kar raha hai.
for message in st.session_state['message_history']:   # ✅ corrected key name
    # now setting the user input to chatmessage component mei.
    with st.chat_message(name=message['role']):
        st.text(message['content'])  # ✅ corrected, no "body" argument in st.text()
        



# defining chat_input box.
user_input = st.chat_input(placeholder="Type Here")

# now setting the user input to chatmessage component mei.
if user_input:
    
    #appending the user input in session state lis
    st.session_state['message_history'].append({'role': "user", 'content': user_input})
    with st.chat_message(name="user"):
        st.text(user_input)
        
     #while invoking first thing we pass initiatial state.
    initial_state = ChatbotState(message=[HumanMessage(content=user_input)],)
    
    
    config1 = {"configurable": {'thread_id':'1'}}
    
    # now setting the AI response to chatmessage component mei.
    with st.chat_message(name="AI"):
        
        #write_stream method --- Iska use tab hota hai jab aapko LLM ka response stream karke dikhana ho
        ai_response_typing = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in workflow.stream(
                input=initial_state,
                config=config1,
                stream_mode="messages"
            )
        )

        
    #appending the AI response in session state lis
    if ai_response_typing.strip():
        st.session_state['message_history'].append({'role': "AI", 'content': ai_response_typing})