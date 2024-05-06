import streamlit as st
from github_repo_fetcher import GitHubRepoFetcher
from github_repo_pusher import GitHubRepoPusher
from llm import llm
import prompts



categories = ['code_documentation', 'inline_commenting', 'code_quality']

selection = st.selectbox('Select the Use Case', categories, placeholder='Use Cases', index=None)


def code_documentation():
    tab1, tab2, tab3 = st.tabs(["Github repo", "Code Documentation", "Upload to GitHub"])
    st.session_state.submitted_to_github = False
    st.session_state.response = ''
    with tab1:
        # Streamlit app title
        st.title("GitHub Repository Code Viewer with Expandable Sections")
        # Text inputs for GitHub username, repository name, file extensions, and optional personal access token
        with st.sidebar:
            owner = st.text_input("GitHub Username", "anurag-singh-9622")
            repo = st.text_input("Repository Name", "code_doc_parody")
            extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
            token = st.text_input("GitHub Personal Access Token (optional)", type="password", value='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')
            api_key = st.text_input("OpenAI api key", type="password", value='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')
            submitted = st.checkbox("Fetch Repository Contents")

        # Button to fetch files with specified extensions
        if submitted:
            try:
                # Convert extensions input into a list
                extensions = [ext.strip() for ext in extensions_input.split(",")]

                # Create GitHubRepoFetcher instance
                fetcher = GitHubRepoFetcher(owner, repo, token)

                # Fetch files from the repository with the specified extensions
                fetcher.fetch_files(extensions)

                # Retrieve fetched contents and all file paths
                list_of_contents = fetcher.get_contents()
                list_all_files = fetcher.get_all_files()
                dict_file_content = {}
                if list_of_contents:
                    st.header(f"Contents of Repository: {repo}")

                # if list_all_files:
                #     # Display the list of all file paths in an expandable section
                #     with st.expander("All Files in Repository"):
                #         st.write(", ".join(list_all_files))
                if list_all_files:
                    st.header("All Files in Repository")
                    options = st.multiselect(
                        'Select the files', list_all_files
                        )

                    # Display the list of all file paths in an expandable section with bullet points
                    with st.expander("Files in Repository"):
                        # Using a formatted string for better readability
                        file_list = "\n".join([f"- {file}" for file in list_all_files])
                        st.text(file_list)  # Displaying as plain text for bullet points        

                    # Display fetched contents in expandable sections
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            with st.expander(f"File: {file_path}"):
                                st.code(content, language="python", line_numbers=True)
                                st.write("-" * 50)  # Separator in Streamlit
                    submitted_to_llm = st.checkbox('Create Documentation')
                            


            except Exception as e:
                # Handle errors and display user-friendly messages
                st.error(f"An error occurred while fetching contents: {str(e)}")
            submitted_to_github = False
            if submitted_to_llm:
                with tab2:
                    doc_assistant = llm(api_key=api_key)
                    total_tokens = 0
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            if not st.session_state.submitted_to_github:
                                st.session_state.response = doc_assistant.llm_response(prompts.prompts(selection, content))
                                total_tokens += st.session_state.response.usage.total_tokens # type: ignore
                                response = st.session_state.response.choices[0].message.content
                            # response = f'Hello, my name is {file_path}'
                            dict_file_content[file_path] = response # Storing the file and corrosponding md response
                            with st.expander(f"File: {file_path}"):
                                response # type: ignore
                                st.write("-" * 50)  # Separator in Streamlit
                    
                with tab1:
                    st.success('Document Successfully Generated, go to tab -> Code Documentation',icon="✅")
                with tab2:
                    st.info('To upload in github, go to tab -> Upload to Github',icon="ℹ️")
                with st.sidebar:
                    st.success(f"total_tokens: {total_tokens}",icon="✅")

            with tab3:
                owner = st.text_input("GitHub Username", "anurag-singh-9622", key = 'github2_owner_input')
                repo = st.text_input("Repository Name", "sample", key = 'github2_repo_input')
                token = st.text_input("GitHub Personal Access Token (optional)", key = 'github2_token_input', type="password", value='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')
                submitted_to_github = st.checkbox('Upload to GitHub')
                if submitted_to_github:
                    st.session_state.submitted_to_github = True
                    try:
                        # Create a GitHubRepoPusher instance
                        pusher = GitHubRepoPusher(owner, repo, token)

                        # Push the files to GitHub
                        commit_message = "Updating files in bulk files."
                        results = pusher.push_files(dict_file_content, commit_message)

                        # Display the results
                        for file_path, result in results.items():
                            print(f"Result for '{file_path}': {result}")
                            with st.expander(label = f'{file_path}'): f"Result for '{file_path}': {result}"

                        if results:
                            st.success('Successfully Pushed to Github',icon="✅")
                            st.link_button("Go to GitHub", f"https://github.com/{owner}/{repo}")
                    except Exception as e:
                        st.error(f"An error occurred while pushing the docs to github: {str(e)}")
                        print(f"An error occurred while pushing the docs to github: {str(e)}")

def inline_commenting():
    tab1, tab2 = st.tabs(["Github repo", "Inline commenting"])
    with tab1:
        # Streamlit app title
        st.title("GitHub Repository Code  Inline commenting with Expandable Sections")
        # Text inputs for GitHub username, repository name, file extensions, and optional personal access token
        with st.sidebar:
            owner = st.text_input("GitHub Username", "anurag-singh-9622")
            repo = st.text_input("Repository Name", "code_doc_parody")
            extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
            token = st.text_input("GitHub Personal Access Token (optional)", type="password", value='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')
            api_key = st.text_input("OpenAI api key", type="password", value='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')
            submitted = st.checkbox("Fetch Repository Contents")

        # Button to fetch files with specified extensions
        if submitted:
            try:
                # Convert extensions input into a list
                extensions = [ext.strip() for ext in extensions_input.split(",")]

                # Create GitHubRepoFetcher instance
                fetcher = GitHubRepoFetcher(owner, repo, token)

                # Fetch files from the repository with the specified extensions
                fetcher.fetch_files(extensions)

                # Retrieve fetched contents and all file paths
                list_of_contents = fetcher.get_contents()
                list_all_files = fetcher.get_all_files()

                if list_of_contents:
                    st.header(f"Contents of Repository: {repo}")

                # if list_all_files:
                #     # Display the list of all file paths in an expandable section
                #     with st.expander("All Files in Repository"):
                #         st.write(", ".join(list_all_files))
                if list_all_files:
                    st.header("All Files in Repository")
                    options = st.multiselect(
                        'Select the files', list_all_files
                        )

                    # Display the list of all file paths in an expandable section with bullet points
                    with st.expander("Files in Repository"):
                        # Using a formatted string for better readability
                        file_list = "\n".join([f"- {file}" for file in list_all_files])
                        st.text(file_list)  # Displaying as plain text for bullet points        

                    # Display fetched contents in expandable sections
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            with st.expander(f"File: {file_path}"):
                                st.code(content, language="python", line_numbers=True)
                                st.write("-" * 50)  # Separator in Streamlit
                    submitted_to_llm = st.checkbox('Create Documentation')
                            


            except Exception as e:
                # Handle errors and display user-friendly messages
                st.error(f"An error occurred while fetching contents: {str(e)}")

            if submitted_to_llm:
                with tab2:
                    doc_assistant = llm(api_key=api_key)
                    total_tokens = 0
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            response = doc_assistant.llm_response(prompts.prompts(selection, content))
                            total_tokens += response.usage.total_tokens
                            response = response.choices[0].message.content
                            with st.expander(f"File: {file_path}"):
                                response
                                st.write("-" * 50)  # Separator in Streamlit
                    with st.sidebar:
                        f"total_tokens: {total_tokens}"

def code_quality():

    tab1, tab2 = st.tabs(["Github repo", "Code Quality"])
    with tab1:
        # Streamlit app title
        st.title("GitHub Repository Code Quality with Expandable Sections")
        # Text inputs for GitHub username, repository name, file extensions, and optional personal access token
        with st.sidebar:
            owner = st.text_input("GitHub Username", "anurag-singh-9622")
            repo = st.text_input("Repository Name", "code_doc_parody")
            extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
            token = st.text_input("GitHub Personal Access Token (optional)", type="password", value='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')
            api_key = st.text_input("OpenAI api key", type="password", value='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')
            submitted = st.checkbox("Fetch Repository Contents")

        # Button to fetch files with specified extensions
        if submitted:
            try:
                # Convert extensions input into a list
                extensions = [ext.strip() for ext in extensions_input.split(",")]

                # Create GitHubRepoFetcher instance
                fetcher = GitHubRepoFetcher(owner, repo, token)

                # Fetch files from the repository with the specified extensions
                fetcher.fetch_files(extensions)

                # Retrieve fetched contents and all file paths
                list_of_contents = fetcher.get_contents()
                list_all_files = fetcher.get_all_files()

                if list_of_contents:
                    st.header(f"Contents of Repository: {repo}")

                # if list_all_files:
                #     # Display the list of all file paths in an expandable section
                #     with st.expander("All Files in Repository"):
                #         st.write(", ".join(list_all_files))
                if list_all_files:
                    st.header("All Files in Repository")
                    options = st.multiselect(
                        'Select the files', list_all_files
                        )

                    # Display the list of all file paths in an expandable section with bullet points
                    with st.expander("Files in Repository"):
                        # Using a formatted string for better readability
                        file_list = "\n".join([f"- {file}" for file in list_all_files])
                        st.text(file_list)  # Displaying as plain text for bullet points        

                    # Display fetched contents in expandable sections
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            with st.expander(f"File: {file_path}"):
                                st.code(content, language="python", line_numbers=True)
                                st.write("-" * 50)  # Separator in Streamlit
                    submitted_to_llm = st.checkbox('Create Documentation')
                            


            except Exception as e:
                # Handle errors and display user-friendly messages
                st.error(f"An error occurred while fetching contents: {str(e)}")

            if submitted_to_llm:
                with tab2:
                    doc_assistant = llm(api_key=api_key)
                    total_tokens = 0
                    for file_path, content in list_of_contents.items():
                        if file_path in options:
                            response = doc_assistant.llm_response(prompts.prompts(selection, content))
                            total_tokens += response.usage.total_tokens
                            response = response.choices[0].message.content
                            with st.expander(f"File: {file_path}"):
                                response
                                st.write("-" * 50)  # Separator in Streamlit
                    with st.sidebar:
                        f"total_tokens: {total_tokens}"

def main():
    try:
        if selection == 'code_documentation':
            code_documentation()
        elif selection == 'inline_commenting':
            inline_commenting()
        elif selection == 'code_quality':
            code_quality()
    except Exception as e:
        # Handle errors and display user-friendly message
        st.error(f"An error occurred while fetching contents: {str(e)}")
        print(f"An error occurred while fetching contents: {str(e)}")

if __name__ == "__main__":
    if selection is not None:
        main()