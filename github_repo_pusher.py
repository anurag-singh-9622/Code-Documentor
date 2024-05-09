from github import Github
import os  # For handling file path manipulations

class GitHubRepoPusher:
    """
    A class to push files to a GitHub repository.
    """

    def __init__(self, owner, repo_name, token):
        self.owner = owner
        self.repo_name = repo_name
        self.token = token
        self.github = Github(token)

    def push_files(self, dict_file_content, commit_message = 'User Commit new changes', extention='.md'):
        """
        Pushes multiple files to a GitHub repository from a dictionary.
        
        :param dict_file_content: A dictionary with file paths as keys and content as values.
        :param commit_message: The commit message for the GitHub push.
        """
        repo = self.github.get_repo(f"{self.owner}/{self.repo_name}")
        results = {}

        for original_file_path, content in dict_file_content.items():
            # Ensure the file has a .md extension
            base_name, _ = os.path.splitext(original_file_path)
            file_path_with_md = f"{base_name}{extention}"

            # Use the new file path with .md extension
            encoded_content = content

            try:
                # Try to get the existing file with the .md extension
                existing_contents = repo.get_contents(file_path_with_md, ref="main")
                # If it exists, update it
                result = repo.update_file(
                    path=existing_contents.path,
                    message=commit_message,
                    content=encoded_content,
                    sha=existing_contents.sha,
                    branch="main",
                )
                results[file_path_with_md] = f"Updated file '{file_path_with_md}'"
            except:
                # If it doesn't exist, create it
                try:
                    result = repo.create_file(
                        path=file_path_with_md,
                        message=commit_message,
                        content=encoded_content,
                        branch="main",
                    )
                    results[file_path_with_md] = f"Created file '{file_path_with_md}'"
                except Exception as e:
                    results[file_path_with_md] = f"Error creating file '{file_path_with_md}': {str(e)}"

        return results
