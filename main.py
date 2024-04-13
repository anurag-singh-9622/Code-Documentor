from openai import OpenAI
import streamlit as st
import random, json
import os
import numpy as np
import time
# from dotenv import load_dotenv

# api_key = st.text_input(':RED[ENTER YOUR API KEY]',placeholder='Insert your api key here')
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')

def llm(promt):
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": """You are a code documentation assistant//\n which helps creating the document for the code for developers.// \n//You will create the document in Markdown format.
            You will provide any suggestion related to improve code with heading 'Suggestions'//"""
            },
            {
            "role": "user",
            "content": f"""Elaborate all the functions, loops, if/else, variables or anything else that might be important and what is its use which you are using in the code.
            code: ```{prompt}```"""
            }

        ],

        temperature=0.8,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
    
        return response


api_key = os.environ['OPENAI_API_KEY_MINE']

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
options = ['Go', "Don't go"]
names = ['Vaibhav', 'Deepu', 'Shantanu', 'Ankit', 'Rahul', 'Apoorv', 'Riya','Rajeev']
# Define weights for each element (higher weight means higher probability)
weights = [3,2,2,1,1,1,6,3]
# Normalize weights to probabilities
probabilities = np.array(weights) / np.sum(weights)

galis = ['bhenchod', 'bosdiwale', 'madharchod', 'gandu', 'ben ka lode', 'chutiye', 'jiska muh lode jaisa']

# Define a format function
def format_func(option):
    return option
 
if not st.session_state.clicked:
    st.session_state.gali = random.choice (galis)
    # Randomly sample from the list with biased probabilities
    st.session_state.random_element = np.random.choice(names, p=probabilities)

# Create the select box with custom formatting
selected_option = st.selectbox('Choose an option:', options, format_func=format_func, index=None, placeholder = "Choose an option", on_change=selected,label_visibility = "collapsed")
if selected_option == "Don't go":
    with st.spinner("Wait for it..."):
        time.sleep(3)
        st.info("chal benchod, mai to jaunga",icon = "ℹ️")

if st.session_state.selected:
    # Display the selected option
    time.sleep(3)
    st.info('Chal code likh '+ f":red[{st.session_state.random_element} {st.session_state.gali}]",icon = "ℹ️")

###########################################################################################
    time.sleep(1)
    # prompt = st.text_area(label="Code input, :red[press Ctrl+Enter after writing code]",placeholder="Write your code here",height=305, on_change=text_input)

    # form container start
    form = st.form(key='my_form')
    # text area in form container
    prompt = form.text_area(label="Code input, :red[press Ctrl+Enter after writing code]",placeholder="Write your code here",height=305)
    # Submit button in form container
    submit_button = form.form_submit_button(label='Submit',on_click=click_button)

    if st.session_state.clicked and len(prompt) > 1:
        # st.button('Submit', on_click=click_button)
        # Generating response from llm
        response = llm(prompt)

        # showing the total tokens used in sidebar
        with st.sidebar:
            f"Total tokens:   {response.usage.total_tokens}"

        # main result from the llm
        result = response.choices[0].message.content

        st.success(f'Ye le {st.session_state.random_element} {random.choice (galis)}') #remove it

        #printing the result
        result
        print(result)


    elif st.session_state.clicked:
        if selected_option is not None: #you can remove this line if not needed
            st.warning('Pura code likh '+ f":red[{st.session_state.random_element} {random.choice (galis)}]") #Change this later


