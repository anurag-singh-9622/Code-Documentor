import os
import requests
import base64
import streamlit as st


listallfile=[]
list_of_contents = {}
# GitHub API endpoint for retrieving contents of a file
# github_api_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
# github_api_url = "https://api.github.com/repos/anurag-singh-9622/Automatic-Irrigation-System/contents/{path}"
def fetch_code_files(owner, repo,file_path=''):
  # Make a url
  github_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
  # Make an API request to fetch contents of the specified file
  response = requests.get(github_api_url.format(owner=owner, repo=repo))

  # Check if request was successful
  if response.status_code == 200:
      # convert the response to JSON format, it comes in a list of dictionary
      list_files = response.json()
      # Iterate through each file in the list
      for file in list_files:
        file_path = file['path']
        if file['type']=='dir':
          fetch_code_files(owner,repo,file_path)
        else:
          url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
          response_of_file = requests.get(url.format(owner=owner, repo=repo, path = file_path)).json()['content']
          decoded_content = base64.b64decode(response_of_file).decode('utf-8')
          list_of_contents.setdefault(file_path, decoded_content)
          listallfile.append(file_path)
        # print(decoded_content)
        # print('*'*150)
        # print(f"Code file '{file_path}' retrieved and saved successfully.")
      
  else:
      print(f"Failed to retrieve code file '{file_path}'. Status code: {response.status_code}")
  # return list_of_contents
# # Example usage
# owner = "anurag-singh-9622"
# repo = "Automatic-Irrigation-System"
# path = "streamlit_chatbot_app.py"
# fetch_code_files(owner, repo, path)



# print(contents)
# Specify the repository details
owner = "anurag-singh-9622"  # Replace with the repository owner's username
repo = "sample"  # Replace with the repository name
# path = "one.py"  # Replace with the path to the file
fetch_code_files(owner, repo)
print(list_of_contents)
# print(listallfile)
# for file,code in contents.items():
  # st.subheader(file)
  # st.code(code, language="python", line_numbers=True)
  # st.write('#'*50)
  # print(code)

for file,code in list_of_contents.items():
  st.subheader(file)
  st.code(code, language="python", line_numbers=True)
  st.write('#'*50)
  print(code)
  print("##"*100)