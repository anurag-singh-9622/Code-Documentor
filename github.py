import requests
import base64
import streamlit as st


class GitHubRepoFetcher:
    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.list_of_contents = {}
        self.list_all_files = []

    def _fetch_contents(self, file_path=""):
        """
        Fetches the contents of files in the repository recursively.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            list_files = response.json()
            for file in list_files:
                current_path = file["path"]
                if file["type"] == "dir":
                    self._fetch_contents(current_path)
                else:
                    content = self._fetch_file_content(current_path)
                    self.list_of_contents[current_path] = content
                    self.list_all_files.append(current_path)
        else:
            print(f"Failed to retrieve code file '{file_path}'. Status code: {response.status_code}")

    def _fetch_file_content(self, file_path):
        """
        Fetches and decodes the content of a specific file in the repository.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{file_path}"
        response = requests.get(github_api_url)
        if response.status_code == 200:
            encoded_content = response.json()["content"]
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            return decoded_content
        else:
            raise Exception(f"Failed to retrieve content for '{file_path}'.")

    def fetch_files(self):
        """
        Initiates the recursive fetching of files from the repository.
        """
        self._fetch_contents()
        return self.list_of_contents

    def display_files(self):
        """
        Displays the fetched files in Streamlit and prints to the console.
        """
        for file, content in self.list_of_contents.items():
            st.subheader(file)
            st.code(content, language="python", line_numbers=True)
            st.write("#" * 50)
            print(content)
            print("##" * 100)


class Main:
    @staticmethod
    def main():
        """
        Main execution point for the script.
        """
        # Specify the repository details
        owner = "anurag-singh-9622"
        repo = "sample"
        list_of_contents = {}
        # Instantiate the GitHubRepoFetcher class
        fetcher = GitHubRepoFetcher(owner, repo)

        # Fetch files from the repository
        list_of_contents = fetcher.fetch_files()

        # Display the fetched files
        # fetcher.display_files()
        for file, content in list_of_contents.items():
            st.subheader(file)
            st.code(content, language="python", line_numbers=True)
            st.write("#" * 50)
            print(content)
            print("##" * 100)
        


if __name__ == "__main__":
    Main.main()
