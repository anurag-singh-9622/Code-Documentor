import os
import requests
import base64
import streamlit as st

# GitHub API endpoint for retrieving contents of a file
# github_api_url = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"
# github_api_url = "https://api.github.com/repos/anurag-singh-9622/Automatic-Irrigation-System/contents/{path}"
def fetch_code_files(owner, repo):
  # Make a url
  github_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
  # Make an API request to fetch contents of the specified file
  response = requests.get(github_api_url.format(owner=owner, repo=repo))

  # Check if request was successful
  if response.status_code == 200:
      # Extract content of the file from the response JSON
      # file_content = response.json().get('content', '')
      # Decode the base64-encoded content
      # decoded_content = base64.b64decode(file_content).decode('utf-8')

      # Save the code file to local filesystem
      # with open(os.path.basename(path), 'w') as file:
          # file.write(decoded_content)
      # print(file_content)
      # print(decoded_content)

      list_files = response.json()
      list_of_contents = {}
      for file in list_files:
        file_path = file['name']
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
        response_of_file = requests.get(url.format(owner=owner, repo=repo, path = file_path)).json()['content']
        decoded_content = base64.b64decode(response_of_file).decode('utf-8')
        list_of_contents.setdefault(file_path, decoded_content)
        # print(decoded_content)
        # print('*'*150)
        print(f"Code file '{file_path}' retrieved and saved successfully.")
  else:
      print(f"Failed to retrieve code file '{path}'. Status code: {response.status_code}")
  return list_of_contents

# Specify the repository details
owner = "anurag-singh-9622"  # Replace with the repository owner's username
repo = "sample"  # Replace with the repository name
path = "one.py"  # Replace with the path to the file
contents = fetch_code_files(owner, repo)

for file,code in contents.items():
  st.subheader(file)
  st.code(code, language="python", line_numbers=True)
  st.write('#'*50)
  print(code)
  print("##"*100)



# print(contents)