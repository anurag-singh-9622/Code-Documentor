import requests
import base64


class GitHubRepoFetcher:
    """
    A class to fetch file contents from all repositories of a given GitHub user.
    """

    def __init__(self, owner):
        """
        Initializes the GitHubRepoFetcher with the owner's GitHub username.
        
        :param owner: GitHub username of the repository owner.
        """
        self.owner = owner
        self.list_of_contents = {}

    def _fetch_contents(self, repo_name, file_path=""):
        """
        Recursively fetches the contents of files in a specified GitHub repository.

        :param repo_name: Name of the GitHub repository.
        :param file_path: Path within the repository to fetch contents from. Defaults to the root.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{file_path}"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            list_files = response.json()
            # Loop through all files and directories
            for file in list_files:
                current_path = file["path"]
                # If it's a directory, fetch contents recursively
                if file["type"] == "dir":
                    self._fetch_contents(repo_name, current_path)
                # Otherwise, fetch the file content
                else:
                    content = self._fetch_file_content(repo_name, current_path)
                    # Store the content in a dictionary with repo and path information
                    self.list_of_contents.setdefault(repo_name, {}).setdefault(current_path, content)
        else:
            # Handle failed API response
            raise Exception(f"Failed to retrieve contents for '{repo_name}/{file_path}'. Status code: {response.status_code}")

    def _fetch_file_content(self, repo_name, file_path):
        """
        Fetches and decodes the content of a specific file in a GitHub repository.

        :param repo_name: Name of the GitHub repository.
        :param file_path: Path of the file to fetch.
        :return: Decoded content of the file.
        """
        github_api_url = f"https://api.github.com/repos/{self.owner}/{repo_name}/contents/{file_path}"
        response = requests.get(github_api_url)
        if response.status_code == 200:
            # Decode the content from Base64 to get the original file content
            encoded_content = response.json()["content"]
            decoded_content = base64.b64decode(encoded_content).decode("utf-8")
            return decoded_content
        else:
            # Raise an exception if the request fails
            raise Exception(f"Failed to retrieve content for '{repo_name}/{file_path}'. Status code: {response.status_code}")

    def fetch_all_files(self):
        """
        Fetches all files from all public repositories owned by a GitHub user.
        """
        github_api_url = f"https://api.github.com/users/{self.owner}/repos"
        response = requests.get(github_api_url)

        if response.status_code == 200:
            # Get the list of repositories
            repos = response.json()
            # Fetch contents for each repository
            for repo in repos:
                repo_name = repo["name"]
                self._fetch_contents(repo_name)
        else:
            # Handle failed API response for fetching repositories
            raise Exception(f"Failed to retrieve repositories for user '{self.owner}'. Status code: {response.status_code}")

    def get_contents(self):
        """
        Returns the fetched file contents from all repositories.

        :return: Dictionary of file contents by repository and file path.
        """
        return self.list_of_contents


def main():
    """
    Main entry point for the script to fetch and display contents from all repositories of a GitHub user.
    """
    owner = "octocat"  # Replace with the GitHub username of interest

    # Create an instance of GitHubRepoFetcher with the specified owner
    fetcher = GitHubRepoFetcher(owner)

    # Fetch all files from all repositories
    fetcher.fetch_all_files()

    # Retrieve the fetched contents
    list_of_contents = fetcher.get_contents()

    # Display the contents for all repositories
    for repo_name, contents in list_of_contents.items():
        print(f"Contents of repository '{repo_name}':")
        for file_path, content in contents.items():
            print(f"File: {file_path}")
            print(content)
            print("=" * 50)


# Ensure this script is being run directly (not imported)
if __name__ == "__main__":
    main()
