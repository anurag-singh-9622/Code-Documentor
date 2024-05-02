from github import Github

#Github personal access token
#https://github.com/settings/apps

def pushToGithub(owner, repo, token):

    g = Github(f'{token}')

    #Github username/repo name
    repo = g.get_repo('ayushchaplot/confluence')

    #reading file and string in into a variable
    with open(r'C:\Users\admin\Desktop\CTS Hackatone\markdown-sample.md', 'r') as file:
        data = file.read()

    #pushing code to github repo
    repo.create_file('documents/markdown-sample.md', 'code documentation uploaded ', data, branch='main')

    print("Document pushed to GitHub successfully...")


# pip install PyGithub
# pip install --upgrade urllib3 chardet requests
