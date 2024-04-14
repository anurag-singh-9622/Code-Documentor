from openai import OpenAI
import streamlit as st
import os
import time
# from dotenv import load_dotenv

    
with st.sidebar:
    st.text_input(':RED[ENTER YOUR API KEY]',key='api_key',placeholder='Insert your api key here', type="password")
api = st.session_state.api_key
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')
st.header('Code Documentation Assistant', divider="blue")

def llm(promt):
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": """You are a code documentation assistant//\n which helps creating the document for the code for developers.// \n//You will create the document in Markdown format.
            You will provide any suggestion related to improve code with heading 'Suggestions'// If you see very absurd code, //don't return anything just return,// ```Please provide correct code```"""
            },
            # {
            # "role": "user",
            # "content": "If you see very absurd code, //don't return anything just return,// ```Please provide correct code```"
            # },
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


# api_key = os.environ['OPENAI_API_KEY_MINE']

client = OpenAI(api_key = api)
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


# Display the selected option
time.sleep(3)

# form container starts from here
form = st.form(key='my_form')
# text area in form container
prompt = form.text_area(label="Code input",placeholder="Write your code here",height=305)
# Submit button in form container

submit_button = form.form_submit_button(label='Submit',on_click=click_button)

if st.session_state.clicked and len(prompt) > 1:
    # Generating response from llm
    response = llm(prompt)

    # showing the total tokens used in sidebar
    with st.sidebar:
        f"Total tokens:   {response.usage.total_tokens}"

    # main result from the llm
    result = response.choices[0].message.content

    st.success("Your Doument is Generated successfully")

    #printing the result
    result
    st.info("If you don't like the result you can submit again to regenrate", icon="ℹ️")
    print(result)


elif st.session_state.clicked:
    st.warning(":red[Please Write Some Code]") #Change this later


