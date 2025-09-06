import streamlit as st

#defining User ke liye the chat_message component of streamlit.
with st.chat_message(name="user"):
    st.text("Hiii") #yeh pe Human message from LLM we can redirect here
    
    
#defining AI ke liye the chat_message component of streamlit.
with st.chat_message(name="AI"):
    st.text("How can assist you today?") #yeh pe AI message from LLM we can redirect here
    

#this component we used to show input box in UI page.
user_input = st.chat_input(placeholder="Type Here")


#now setting the user input  to chatmessage component mei.
if user_input:
    with st.chat_message(name="user"):
        st.text(body=user_input)