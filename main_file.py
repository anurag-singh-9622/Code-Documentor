import streamlit as st
from github_repo_fetcher import GitHubRepoFetcher
from github_repo_pusher import GitHubRepoPusher
from push_to_confluence import confluence
from llm import LLM
from rag_llm import llm_response
from prompts import prompts
import traceback
import os
st.set_page_config(page_title = "Code Documentor",page_icon="🧊", layout="wide", initial_sidebar_state="expanded") 

# Constants for default values
DEFAULT_GITHUB_USERNAME = "anurag-singh-9622"
DEFAULT_REPO_NAME = "sample"
DEFAULT_EXTENSIONS = ".py, .md"


st.title("Code Documentor")
real_use_case = ['github_repo_code_documentation', 'individual_code_documentation']

# selection_real_use_case = st.selectbox("select", real_use_case, format_func=lambda a : (a[0].upper() + a[1:]).replace("_", " "), index=None)
selection_real_use_case = st.selectbox('Select the Use Case', real_use_case, index=None, placeholder="Select the Use Cases here", help="These are the use cases", format_func=lambda a : (a[0].upper() + a[1:]).replace("_", " "))



def seprate_code_documentation():
    tab1, tab2, tab3 = st.tabs(["Generated Documentation", "Upload to GitHub", "Upload to Confluence"])
    with tab1:
        st.title("Generate Documentation")
        code_input = st.text_area('Write or Paste your code here for documentation, inline commenting or code quality', placeholder='Write code here')
        context = st.text_area("Write the description of the code", placeholder="Write the elaborated description of the code, with detailed descirption of every part of the code.")
        submited_code = st.checkbox('Submit Code')
        dict_file_content_individual = {}
        # total_tokens = 0
        if submited_code:
            with st.sidebar:
                # categories = ['code_documentation', 'inline_commenting', 'code_quality']
                # task = st.selectbox('Select a task', categories)
                api_key = st.text_input("OpenAI API key", type="password")
                file_name = st.text_input('Write your filename with extention', 'sample.py')
                submitted = st.checkbox("Generate Documentation")
                base_name, default_ext = os.path.splitext(file_name)
                
                if task == 'code_documentation':
                    extention = '.md'
                elif task == 'inline_commenting':
                    extention = default_ext
                elif task == 'code_quality':
                    extention = '.md'
                
            if submitted:
                # llm = LLM(api_key=api_key)
                prompt = prompts(task)
                print(f"-----------------------------------------------Prompt = {prompt}--------------------------------------")
                response = llm_response(api_key=api_key, prompt=prompt, context=context, code=code_input)

                # total_tokens += response.usage.total_tokens # type: ignore
                response_content = response
                print("-----------------------------------------------START OF SEPERATE CODE DOCUMENTATION--------------------------------------")
                print(f"-----------------------------------------------response = {response_content}--------------------------------------")
                dict_file_content_individual[file_name] = response_content
                print(f"-----------------------------------------------dict_file_content_individual = {dict_file_content_individual}--------------------------------------")
                with st.expander(f'{base_name}{extention}'):
                    response_content
                if response:
                    st.success("Documentation generated", icon="✅")
                    # st.sidebar.success(f"Total tokens used: {total_tokens}", icon="✅") # type: ignore
                    # Store in session state for later use
                    st.session_state.dict_file_content_individual = dict_file_content_individual
                    st.info('To upload in github, go to tab -> Upload to Github',icon="ℹ️")

    with tab2:
        st.header("Upload to GitHub")
        st.write('Fill this if you want to upload in GitHub')
        owner, repo, token = collect_github_inputs("Upload")


        if 'dict_file_content_individual' in st.session_state and st.session_state.dict_file_content_individual:
            if st.checkbox("Upload to GitHub"):
                results = upload_to_github(owner, repo, token, st.session_state.dict_file_content_individual, selection=task)
                if results:
                    st.success("Successfully uploaded to GitHub", icon="✅")
                    for file_path, result in results.items():
                        with st.expander(f"{file_path}"):
                            st.text(f"Result: {result}")

                st.link_button("Go to GitHub",f'https://github.com/{owner}/{repo}/')

    with tab3:
        if task == "code_documentation" or task == "inline_commenting" or task == "code_quality":
            st.header("Upload to Confluence")
            confluence_url = st.text_input("Confluence URL", placeholder="Add the Confluence URL here")  
            space_key = st.text_input("Space Key", placeholder="Add the Space key here")  
            username = st.text_input("User Name", placeholder="Add your username here")   
            api_token = st.text_input("API Key", placeholder="Add the api token here")
            
            if st.checkbox("Upload to Conflunce"):
                for file_path, content in st.session_state.dict_file_content_individual.items():
                    confluence(confluence_url,space_key,username,api_token,file_path,content)
        else:
            st.warning("Error in selecting the correct option", icon="⚠️")

        
# Function to collect GitHub input details
def collect_github_inputs(suffix=''):
    """
    Collects GitHub inputs like owner, repository, and token from the user.
    """
    owner = st.text_input(f"GitHub Username {suffix}", DEFAULT_GITHUB_USERNAME, key=f'github_owner_{suffix}')
    repo = st.text_input(f"Repository Name {suffix}", DEFAULT_REPO_NAME, key=f'github_repo_{suffix}')
    token = st.text_input("GitHub Personal Access Token", key=f'github_token_{suffix}', type="password")

    return owner, repo, token

# Function to fetch repository contents
def fetch_repository_contents(owner, repo, extensions, token):
    """
    Fetches repository contents based on given owner, repository, extensions, and token.
    """
    try:
        fetcher = GitHubRepoFetcher(owner, repo, token)
        fetcher.fetch_files(extensions)
        list_of_contents = fetcher.get_contents()
        list_all_files = fetcher.get_all_files()
        return list_of_contents, list_all_files
    except Exception as e:
        st.error(f"Error fetching repository contents: {str(e)}")
        traceback.print_exc()
        return {}, []

# Function to generate documentation using LLM
@st.cache_data(show_spinner=True)
def generate_documentation(list_of_contents, selected_files:list, api_key:str, prompt_type:str, context_dict:dict):
    """
    Generates documentation for the selected files using a large language model (LLM).
    :param list_of_contents: A dict having file path as key and code as its key
    :param selected_files: A list of files that user selected
    :param api_key: LLM api key
    :param prompt_type: It is the type of prompt, like prompt for code documentatio, or inline commenting or code quality
    """
    try:
        # doc_assistant = LLM(api_key=api_key)
        dict_file_content = {} #A dict having file path as key and the markdown response as its key
        prompt = prompts(prompt_type)
        print(f"------------------------------------prompt = {prompt}-----------------------------------------------------")
        for file_path, code in list_of_contents.items():
            if file_path in selected_files:
                print(f"-------------------------------------------CODE: {code}--------------------------------------------------------")
                context = context_dict[file_path]
                print(f"--------------------------------------------CONTEXT: {context}-----------------------------------------")
                response_content = llm_response(api_key=api_key, prompt=prompt, context = context, code=code)
                dict_file_content[file_path] = response_content

        return dict_file_content

    except Exception as e:
        st.error(f"Error generating documentation: {str(e)}")
        traceback.print_exc()
        return {}

def upload_to_github(owner, repo, token, dict_file_content: dict, selection):
    try:
        # Create a GitHubRepoPusher instance
        pusher = GitHubRepoPusher(owner, repo, token)
        extention = '.md'

        if selection == 'code_documentation':
            extention = '.md'
        elif selection == 'inline_commenting':
            extention = '.py'
        elif selection == 'code_quality':
            extention = '.md'

        # Push the files to GitHub
        commit_message = "Updating files in bulk."
        results = pusher.push_files(dict_file_content, commit_message, extention=extention)

        # Display the results
        # for file_path, result in results.items():
        #     print(f"Result for '{file_path}': {result}")
        #     with st.expander(label = f'{file_path}'): f"Result for '{file_path}': {result}"

    except Exception as e:
        st.error(f"An error occurred while pushing the docs to github: {str(e)}")
        print(f"An error occurred while pushing the docs to github: {str(e)}")
    return results

# Main Streamlit function
def code_documentation():
    tab1, tab2, tab3, tab4 = st.tabs(["GitHub Repo", "Generated Documentation", "Upload to GitHub", "Upload to Confluence"])

    # Tab 1: Fetch repository contents and generate documentation
    with tab1:
        st.title("GitHub Repository Code Viewer")

        with st.sidebar:
            owner, repo, token = collect_github_inputs()
            extensions_input = st.text_input("File Extensions (comma-separated)", DEFAULT_EXTENSIONS)
            api_key = st.text_input("OpenAI API key", type="password")
            submitted = st.checkbox("Fetch Repository Contents")

        if submitted:
            extensions = [ext.strip() for ext in extensions_input.split(",")]
            list_of_contents, list_all_files = fetch_repository_contents(owner, repo, extensions, token)
            dict_of_desc = {} #dict containing the file path as key and its description as the value
            dict_file_content = {} ##dict containing the file path as key and llm response as the value

            if list_all_files:
                selected_files = st.multiselect("Select files", list_all_files)

                for file_path, content in list_of_contents.items():
                        if file_path in selected_files:
                            dict_of_desc[file_path] = st.text_area(f"Enter the description for {file_path}", key = file_path, placeholder="Write the elaborated description of the code, with detailed descirption of every part of the code.")
                            with st.expander(f"File: {file_path}"):
                                st.code(content, language="python", line_numbers=True)
                            

                # Generate documentation based on selected files
                if st.checkbox("Generate Documentation"):
                    try:
                        prompt_type = selection.lower().replace(" ", "_")  # type: ignore # Use the selected use case
                        print(f"------------------------------------------------------------------------prompt_type = {prompt_type} -----------------------------------------------------------")
                    except:
                        st.warning('Select a task', icon="⚠️")
                    
                    dict_file_content = generate_documentation(list_of_contents, selected_files, api_key, prompt_type, context_dict = dict_of_desc)

                    # Store in session state for later use
                    st.session_state.dict_file_content = dict_file_content

                    st.success("Documentation generated, go to tab -> Generated Documentation", icon="✅")
                    # st.sidebar.success(f"Total tokens used: {total_tokens}", icon="✅")

    # Tab 2: Display generated documentation
    with tab2:
        st.header("Generated Documentation")
        if 'dict_file_content' in st.session_state and st.session_state.dict_file_content:
            for file_path, content in st.session_state.dict_file_content.items():
                with st.expander(f"{file_path}"):
                    st.markdown(content)
                    st.write("-" * 50)
        st.info('To upload in github, go to tab -> Upload to Github',icon="ℹ️")

    # Tab 3: Inputs for GitHub and upload option
    with tab3:
        st.header("Upload to GitHub")
        owner, repo, token = collect_github_inputs("Upload")

        if 'dict_file_content' in st.session_state and st.session_state.dict_file_content:
            if st.checkbox("Upload to GitHub"):
                results = upload_to_github(owner, repo, token, st.session_state.dict_file_content, selection=selection)

                if results:
                    st.success("Successfully uploaded to GitHub", icon="✅")
                    for file_path, result in results.items():
                        with st.expander(f"{file_path}"):
                            st.text(f"Result: {result}")

                st.link_button("Go to GitHub",f'https://github.com/{owner}/{repo}/')  # Refresh to reset states
    
    with tab4:
        if selection == "code_documentation" or selection == "inline_commenting" or selection == "code_quality":
            st.header("Upload to Confluence")
            confluence_url = st.text_input("Confluence URL", placeholder="Add the Confluence URL here")  
            space_key = st.text_input("Space Key", placeholder="Add the Space key here")  
            username = st.text_input("User Name", placeholder="Add your username here")   
            api_token = st.text_input("API Key", placeholder="Add the api token here")
            
            if st.checkbox("Upload to Conflunce"):
                for file_path, content in st.session_state.dict_file_content.items():
                    confluence(confluence_url,space_key,username,api_token,file_path,content)
        else:
            st.warning("Error in selecting the correct option", icon="⚠️")


# Main execution block with error handling
try:
    if selection_real_use_case == 'github_repo_code_documentation':
        # Set up the use case selection at the top
        categories = ['code_documentation', 'inline_commenting', 'code_quality']
        selection = st.radio('Select the task', categories, index=None)
        if selection: code_documentation()
    elif selection_real_use_case == 'individual_code_documentation':
        categories = ['code_documentation', 'inline_commenting', 'code_quality']
        task = st.radio('Select the task', categories, index=None)
        if task: seprate_code_documentation()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    print(f"An error occurred: {str(e)}")
