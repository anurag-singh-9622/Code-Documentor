from github import Github
import base64


class GitHubRepoPusher:
    """
    A class to push files to a GitHub repository.
    """

    def __init__(self, owner, repo_name, token):
        self.owner = owner
        self.repo_name = repo_name
        self.token = token
        self.github = Github(token)

    def push_files(self, dict_file_content, commit_message):
        """
        Pushes multiple files to a GitHub repository from a dictionary.
        
        :param dict_file_content: A dictionary with file paths as keys and content as values.
        :param commit_message: The commit message for the GitHub push.
        """
        repo = self.github.get_repo(f"{self.owner}/{self.repo_name}")
        results = {}

        for file_path, content in dict_file_content.items():
            # encoded_content = base64.b64encode(content.encode()).decode()
            encoded_content = content
            # Check if the file exists
            try:
                existing_contents = repo.get_contents(file_path, ref="main")
                if isinstance(existing_contents, list):
                    # If it's a list, we need to find the exact file
                    for item in existing_contents:
                        if item.path == file_path:
                            existing_file = item
                            break
                else:
                    existing_file = existing_contents

                # If the file exists, update it
                result = repo.update_file(
                    path=existing_file.path,
                    message=commit_message,
                    content=encoded_content,
                    sha=existing_file.sha,
                    branch="main",
                )
                results[file_path] = f"Updated file '{file_path}'"

            except:
                # If it doesn't exist, create it
                try:
                    result = repo.create_file(
                        path=file_path,
                        message=commit_message,
                        content=encoded_content,
                        branch="main",
                    )
                    results[file_path] = f"Created file '{file_path}'"
                except Exception as e:
                    results[file_path] = f"Error creating file '{file_path}': {str(e)}"

        return results
