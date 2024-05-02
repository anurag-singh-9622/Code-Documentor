import requests
import base64
import streamlit as st


class GitHubRepoFetcher:
    """
    A class to fetch file contents from a GitHub repository with optional filtering by file extension.
    """

    def __init__(self, owner, repo, token=None):
        """
        Initializes the GitHubRepoFetcher with the GitHub owner's username, repository name, and optional personal access token.

        :param owner: GitHub username of the repository owner.
        :param repo: Name of the GitHub repository.
        :param token: Optional GitHub personal access token for authentication.
        """
        self.owner = owner
        self.repo = repo
        self.token = token
        self.headers = {"Authorization": f"token {token}"} if token else {}
        self.list_of_contents = {}
        self.list_all_files = []

    def _fetch_contents(self, extensions, file_path=""):
        """
        Recursively fetches contents from the given GitHub repository, only for specific file extensions.
        
        :param extensions: A list of file extensions to include (e.g., ['.py', '.txt']).
        :param file_path: The starting file path within the repository. Defaults to the root.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        response = requests.get(github_api_url, headers=self.headers)

        if response.status_code == 200:
            list_files = response.json()  # List of files and directories

            for file in list_files:
                current_path = file["path"]

                if file["type"] == "dir":
                    self._fetch_contents(extensions, current_path)  # Recursive fetch
                elif any(current_path.endswith(ext) for ext in extensions):
                    content = self._fetch_file_content(current_path)  # Fetch content
                    self.list_of_contents[current_path] = content
                    self.list_all_files.append(current_path)
        else:
            raise Exception(f"Failed to retrieve '{file_path}' with status code: {response.status_code}")

    def _fetch_file_content(self, file_path):
        """
        Fetches and decodes the content of a specific file in the repository.

        :param file_path: The path of the file to fetch.
        :return: Decoded content of the file.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        response = requests.get(github_api_url, headers=self.headers)

        if response.status_code == 200:
            encoded_content = response.json()["content"]
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            return decoded_content
        else:
            raise Exception(f"Failed to retrieve content for '{file_path}'. Status code: {response.status_code}")

    def fetch_files(self, extensions):
        """
        Fetches files from the repository with specified extensions.

        :param extensions: A list of file extensions to include (e.g., ['.py', '.txt']).
        """
        self.list_all_files.clear()  # Clear previous list
        self._fetch_contents(extensions)  # Start fetching from the root

    def get_contents(self):
        """
        Returns the dictionary of file contents.
        
        :return: Dictionary with file paths as keys and their content as values.
        """
        return self.list_of_contents

    def get_all_files(self):
        """
        Returns the list of all file paths fetched from the repository.
        
        :return: List of all file paths.
        """
        return self.list_all_files

    def display_files(self):
        """
        Displays the fetched files in Streamlit and prints their content to the console.
        """
        for file, content in self.list_of_contents.items():
            st.subheader(file)  # Display the file path as a subheader
            st.code(content, language="python", line_numbers=True)
            st.write("-" * 50)  # Separator in Streamlit
            print(content)  # Print to console
            print("##" * 100)  # Console separator
    
    


class Main:
    """
    A class with a static `main()` method to serve as the entry point for a Streamlit-based application.
    """

    @staticmethod
    def main():
        """
        The main entry point for the Streamlit app, allowing user input for GitHub repository details
        and fetching specific files based on provided extensions.
        """
        st.title("GitHub Repository Code Viewer")

        # Text inputs for GitHub username, repository name, file extensions, and optional personal access token
        owner = st.text_input("GitHub Username", "octocat")
        repo = st.text_input("Repository Name", "Hello-World")
        extensions_input = st.text_input("File Extensions (comma-separated)", ".py, .md")
        token = st.text_input("GitHub Personal Access Token (optional)", type="password")

        if st.button("Fetch Repository Contents"):
            try:
                # Convert the extensions input into a list of extensions
                extensions = [ext.strip() for ext in extensions_input.split(",")]

                # Create an instance of GitHubRepoFetcher with or without a token
                fetcher = GitHubRepoFetcher(owner, repo, token)

                # Fetch files from the repository with the specified extensions
                fetcher.fetch_files(extensions)

                # Retrieve the fetched contents and the list of all files
                list_of_contents = fetcher.get_contents()
                list_all_files = fetcher.get_all_files()
                
                # Display list of all file paths
                if list_all_files:
                    st.header("All Files in Repository")
                    st.write(", ".join(list_all_files))

                # Display the fetched contents
                if list_of_contents:
                    st.header(f"Contents of Repository: {repo}")
                    for file_path, content in list_of_contents.items():
                        st.subheader(f"File: {file_path}")
                        st.code(content, language="python", line_numbers=True)
                        st.write("-" * 50)  # Separator in Streamlit


            except Exception as e:
                # Handle errors and display user-friendly message
                st.error(f"An error occurred while fetching contents: {str(e)}")


# Run the static `main()` method
if __name__ == "__main__":
    Main.main()