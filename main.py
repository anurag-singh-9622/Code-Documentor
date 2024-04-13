from openai import OpenAI
import streamlit as st
import random, json
import os
# from dotenv import load_dotenv

# api_key = st.text_input(':RED[ENTER YOUR API KEY]',placeholder='Insert your api key here')
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')
api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key = api_key)
# with open('doc.json') as file:
#     # Step 2: Parse the JSON data
#     data = json.load(file) something
if 'text' not in st.session_state:
    st.session_state.text = False

def text_input():
    st.session_state.text = True

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if 'selected' not in st.session_state:
    st.session_state.selected = False

def selected():
    st.session_state.selected = True
###########################################################################################
#Adding gali sentences
names = ['Vaibhav', 'Deepu', 'Shantanu', 'Ankit', 'Rahul', 'Apoorv', 'Riya']
galis = ['bhenchod', 'bosdiwale', 'madharchod', 'gandu', 'ben ka loda', 'chutia', 'jiska muh lode jaisa']

# Define a format function
def format_func(option):
    return option
 
if not st.session_state.clicked:
    st.session_state.gali = random.choice (galis)

# Create the select box with custom formatting
selected_option = st.selectbox('Choose an option:', names, format_func=format_func, index=None, placeholder = "Choose an option", on_change=selected)

if st.session_state.selected:
    # Display the selected option
    st.write('Chal code likh', f":red[{selected_option} {st.session_state.gali}]")

###########################################################################################





prompt = st.text_area(label="Code input",placeholder="Write your code here",height=305, on_change=text_input)

def llm(promt):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "system",
        "content": """You are a code documentation assistant//\n which helps creating the document for the code for developers.// \n//You will create the document in Markdown format.
        You will provide any suggestion related to improve code,// You will provide inline comment of the code//"""
        },
        {
        "role": "user",
        "content": f"""Elaborate all the functions, loops, if/else, variables or anything else that might be important and what is its use which you are using in the code.
         code: ```{prompt}```"""
        }

    ],

    temperature=0.8,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
 
    return response


if st.session_state.text and len(prompt) > 1:
    st.button('Submit', on_click=click_button)
    if st.session_state.clicked:
        response = llm(prompt)

        with st.sidebar:
            f"Total tokens:   {response.usage.total_tokens}"
        result = response.choices[0].message.content
        st.success(f'Ye le {selected_option} {random.choice (galis)}')
        result
        print(result)
elif st.session_state.text:
    if selected_option is not None: #you can remove this line if not needed
        st.warning('Pura code likh '+ f":red[{selected_option} {random.choice (galis)}]")


