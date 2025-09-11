#importing Module.
import streamlit as st


# ✅ Final Summary:
# Widget inputs clickable hote hain — click par tum condition check karke koi action perform kar sakte ho, jaise if st.button():.
# with tab use karte hain jab tum multiple widgets ko ek saath group karna chahte ho, jaise form ya sidebar.
# Click ke baad result dikhane ke liye st.write() zyada smart aur useful hai, jabki st.text() sirf simple text dikhata hai.
# Agar tum chaho to main tumhare use case ke hisaab se ek complete example bana kar de doon! Bata do tum kya karna chahte ho UI mein.


#want to click the button in UI page.
click = st.button(label = "click Button")
if click:
    st.text(body=True)


#to show download button on UI Page
import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def get_data():
    df = pd.DataFrame(
        np.random.randn(50, 20), columns=("col %d" % i for i in range(20))
    )
    return df

@st.cache_data
def convert_for_download(df):
    return df.to_csv().encode("utf-8")

df = get_data()
csv = convert_for_download(df)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
    icon=":material/download:",
)


#to show submit button icon in FORM.
# Form create kar rahe hain, iska naam "my_form"
with st.form("my_form"):
    # Form ke andar inputs likho
    name = st.text_input("Apna naam likho")
    age = st.number_input("Apni umar likho", min_value=0, max_value=100)
    
    # Submit button bhi form ke andar hi hona chahiye
    submit = st.form_submit_button("Submit karo")
    
# Agar submit hua to result dikhao
    if submit:
        st.write(f"Hello {name}, tumhari umar {age} saal hai!")
        
        
        
        

# CHECKBOX
st.title("Multiple Options Checkbox Example")

# Har option ke liye alag checkbox
option1 = st.checkbox("Option 1")
option2 = st.checkbox("Option 2")
option3 = st.checkbox("Option 3")

# Selected options ko dikhao
st.write("Selected options:")
if option1:
    st.write("Option 1 selected")
if option2:
    st.write("Option 2 selected")
if option3:
    st.write("Option 3 selected")
    
    
    
option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)

st.write("You selected:", option)



#first refering some basic fuctions in streamlit known as TEXT ELEMENT
#title:- to show title of web application
st.title(body = "Here we can give title of My web Application")

#header:- to show header of web application
st.header(body = "this is the header of my web application",divider='red') #to underline the header we used divider

#subheader: is same as header but only one difference is fontsize will small compare to header
st.subheader(body = 'machine learning')

#to show the information details on web page or UI 
st.info(body="information details of users.",icon="🔥")

#if i want to show warning message over UI
st.warning(body="to show warning message for user")


#if i want to show the python code to UI page.
code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code,language='python',)


#if i want to take the input from user
user_input = st.chat_input(placeholder="your message")

#if i want to display some textual content to UI page.
st.text(body="write here")


#to show error message inUI page.
st.error(body="wrong Password")

#to show corrected message in UI page.
st.success(body='correct password')



#to show markdown in UI page.
st.markdown(body="# streamlit is fuck all application")
st.markdown(body="## streamlit is fuck all application")
st.markdown(body="### streamlit is fuck all application")

st.badge("New")
st.badge("Success", icon=":material/check:", color="green")


st.caption("This is a string that explains something above.")


#Display mathematical expressions formatted as LaTeX.
math  = r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    '''
st.latex(body=math)