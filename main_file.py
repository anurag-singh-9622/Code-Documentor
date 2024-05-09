import streamlit as st
from github_repo_fetcher import GitHubRepoFetcher
from github_repo_pusher import GitHubRepoPusher
from llm import LLM
import prompts
import traceback


# Constants for default values
DEFAULT_GITHUB_USERNAME = "anurag-singh-9622"
DEFAULT_REPO_NAME = "code_doc_parody"
DEFAULT_EXTENSIONS = ".py, .md"

# Set up the use case selection at the top
categories = ['code_documentation', 'inline_commenting', 'code_quality']
selection = st.selectbox('Select the Use Case', categories, placeholder='Choose a Use Case', index=None)

# Function to collect GitHub input details
def collect_github_inputs(suffix=''):
    """
    Collects GitHub inputs like owner, repository, and token from the user.
    """
    owner = st.text_input(f"GitHub Username {suffix}", DEFAULT_GITHUB_USERNAME, key=f'github_owner_{suffix}')
    repo = st.text_input(f"Repository Name {suffix}", DEFAULT_REPO_NAME, key=f'github_repo_{suffix}')
    token = st.text_input("GitHub Personal Access Token (optional)", key=f'github_token_{suffix}', type="password")

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
def generate_documentation(list_of_contents, selected_files, api_key, prompt_type):
    """
    Generates documentation for the selected files using a large language model (LLM).
    """
    try:
        doc_assistant = LLM(api_key=api_key)
        dict_file_content = {}
        total_tokens = 0

        for file_path, content in list_of_contents.items():
            if file_path in selected_files:
                response = doc_assistant.llm_response(prompts.prompts(prompt_type, content))
                total_tokens += response.usage.total_tokens # type: ignore
                response_content = response.choices[0].message.content
                dict_file_content[file_path] = response_content

        return dict_file_content, total_tokens

    except Exception as e:
        st.error(f"Error generating documentation: {str(e)}")
        traceback.print_exc()
        return {}, 0

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
        commit_message = "Updating files in bulk files."
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
    tab1, tab2, tab3 = st.tabs(["GitHub Repo", "Generated Documentation", "Upload to GitHub"])

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

            if list_all_files:
                selected_files = st.multiselect("Select files", list_all_files)

                for file_path, content in list_of_contents.items():
                        if file_path in selected_files:
                            with st.expander(f"File: {file_path}"):
                                st.code(content, language="python", line_numbers=True)

                # Generate documentation based on selected files
                if st.checkbox("Generate Documentation"):
                    prompt_type = selection.lower().replace(" ", "_")  # type: ignore # Use the selected use case
                    dict_file_content, total_tokens = generate_documentation(list_of_contents, selected_files, api_key, prompt_type)

                    # Store in session state for later use
                    st.session_state.dict_file_content = dict_file_content

                    st.success("Documentation generated, go to tab -> Generated Documentation", icon="✅")
                    st.sidebar.success(f"Total tokens used: {total_tokens}", icon="✅")

    # Tab 2: Display generated documentation
    with tab2:
        st.header("Generated Documentation")
        if 'dict_file_content' in st.session_state and st.session_state.dict_file_content:
            for file_path, content in st.session_state.dict_file_content.items():
                with st.expander(f"{file_path}"):
                    st.text(content)
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


# Main execution block with error handling
try:
    if selection:
        code_documentation()
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    print(f"An error occurred: {str(e)}")
