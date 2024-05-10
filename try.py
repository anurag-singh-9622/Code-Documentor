import streamlit as st

from openai import OpenAI
import webbrowser
client = OpenAI(
    organization='org-CymJVeTtMPU7CBRWNjHzRaJt'
    )
# # Call the API
# response = client.images.generate(
#   model="dall-e-3",
#   prompt="a cute cat with a hat on and a logo of cognizant company on a hat",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )

# Show the result that has been pushed to an url
# webbrowser.open(response.data[0].url) # type: ignore
# print(response)

message = [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
content = ''
total_tokens = 0
total_input_tokens = 0
total_output_tokens = 0
while content != 'exit':
  
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    # model = "gpt-4",
    messages=message # type: ignore
  )
  response = completion.choices[0].message.content
  tokens = completion.usage.total_tokens # type: ignore
  input_tokens = completion.usage.prompt_tokens # type: ignore
  output_tokens = completion.usage.completion_tokens # type: ignore
  total_tokens += tokens
  total_input_tokens += input_tokens
  total_output_tokens += output_tokens
  print(f'''{response} 
        TOkens info:
        input_token = {input_tokens} and output_tokens = {output_tokens} and token = {tokens} || 
        total_input_tokes = {total_input_tokens} and total_output_tokens = {total_output_tokens} and total_tokens = {total_tokens}''')
  content = input('Chat: ')
  # print(message)
  if content:
    dict1 = {"role": 'assistant', "content": response}
    message.append(dict1)
    dict1 = {"role": 'user', "content": content}
    message.append(dict1)















# def seprate_code_documentation():
#     tab1, tab2 = st.tabs(["Generated Documentation", "Upload to GitHub"])
#     with tab1:
#         st.title("Generate Documentation")
#         code_input = st.text_area('Write or Paste your code here for documentation, inline commenting or code quality', placeholder='Write code here')
#         submited_code = st.checkbox('Submit Code')
#         dict_file_content = {}
#         total_tokens = 0
#         list_of_contents = {}
#         selected_files = []
#         if submited_code:
#             with st.sidebar:
#                 categories = ['code_documentation', 'inline_commenting', 'code_quality']
#                 selection = st.multiselect('Select one or more tasks', categories)
#                 api_key = st.text_input("OpenAI API key", type="password")
#                 file_name = st.text_input('Write your filename with extention', 'sample.py')
#                 submitted = st.checkbox("Generate Documentation")
#                 list_of_contents[file_name] = code_input
#                 selected_files.append(file_name)
#                 #generate_documentation(list_of_contents, selected_files:list, api_key:str, prompt_type:str)
#             if submitted:
#                 for task in selection:
#                     dict_file_content, total_tokens = generate_documentation(list_of_contents, selected_files, api_key, task)
#                 if dict_file_content:
#                     st.success("Documentation generated, go to tab -> Generated Documentation", icon="✅")
#                     st.sidebar.success(f"Total tokens used: {total_tokens}", icon="✅") # type: ignore
#                     # Store in session state for later use
#                     st.session_state.dict_file_content = dict_file_content
#                     if 'dict_file_content' in st.session_state and st.session_state.dict_file_content:
#                             for file_path, content in st.session_state.dict_file_content.items():
#                                 with st.expander(f"{file_path}"):
#                                     st.text(content)
#                                     st.write("-" * 50)
#                     st.info('To upload in github, go to tab -> Upload to Github',icon="ℹ️")

#     with tab2:
#         st.header("Upload to GitHub")
#         st.write('Fill this if you want to upload in GitHub')
#         owner, repo, token = collect_github_inputs("Upload")

#         if 'dict_file_content' in st.session_state and st.session_state.dict_file_content:
#             if st.checkbox("Upload to GitHub"):
#                 results = upload_to_github(owner, repo, token, st.session_state.dict_file_content, selection=selection)
#                 if results:
#                     st.success("Successfully uploaded to GitHub", icon="✅")
#                     for file_path, result in results.items():
#                         with st.expander(f"{file_path}"):
#                             st.text(f"Result: {result}")

#                 st.link_button("Go to GitHub",f'https://github.com/{owner}/{repo}/')