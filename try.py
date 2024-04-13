# import streamlit as st
# import random

# names = ['Vaibhav', 'Deepu', 'Shantanu']
# gali = ['bhenchod', 'bosdiwala', 'madharchod', 'gandu', 'ben ka loda', 'chutia']
# # Define a format function
# def format_func(option):
#     return option
 
# # Create the select box with custom formatting
# selected_option = st.selectbox('Choose an option:', names, format_func=format_func)
 
# gali_text = random.choice (gali)
# # Display the selected option
# st.write('You selected:', f":red[{selected_option} {gali_text}]")
import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('HELLO'))
