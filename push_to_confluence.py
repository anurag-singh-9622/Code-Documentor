import requests
import json
import base64
import markdown
import streamlit as st


def clear_submit():
    st.session_state["submit"] = True

# function
def confluence(confluence_url,space_key,username,api_token,page_title,mark_data):
    
    #reading file and string in into a variable
    # with open(uploaded_file.name, 'r') as file:
    #     mark_data = file.read()
        
    # Convert markdown to HTML
    html_text = markdown.markdown(mark_data)
    
    # Prepare data for the API request
    data = {
        "type": "page",
        "title": page_title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": html_text,
                "representation": "storage"
            }}}

    url = f"{confluence_url}/rest/api/content"
    # Send the POST request to create the page
    headers = {
    "Authorization": f"Basic {base64.b64encode(f'{username}:{api_token}'.encode()).decode()}",
    "X-Atlassian-Token": api_token,"Content-Type": "application/json"}


    response = requests.post(url, json=data, headers=headers)
    print(response.status_code)

    # Check for success
    if response.status_code == 200:
        st.success(f"{page_title} created successfully!", icon="✅")
        print("Page created successfully!")
    elif response.status_code == 400:
        st.error(f"{page_title} already exist:")
        print("Error creating page:", response.text)
    else:
        st.write("Error creating page:", response.text)
        print("Error creating page:", response.text)


# calling function with inputs
# with st.sidebar:
       
#     confluence_url = st.text_input("Confluence URL", )  
#     space_key = st.text_input("Space Key", )  
#     username = st.text_input("User Name", )   
#     api_token = st.text_input("API Key", ) 
#     page_title = st.text_input("Page Title", ) 
    # uploaded_file = st.file_uploader("Upload file",type=['txt','md'],help="Only txt,md  files are supported",)   
    
# if uploaded_file:
#     confluence(confluence_url,space_key,username,api_token,page_title,uploaded_file)