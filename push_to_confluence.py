import requests

# Set the Confluence URL, username, and password
CONFLUENCE_URL = "https://<your-confluence-url>"
USERNAME = "<your-username>"
PASSWORD = "<your-password>"

# Set the path to the file you want to upload
FILE_PATH = "/path/to/file.txt"

# Create a session
session = requests.Session()

# Authenticate to Confluence
session.auth = (USERNAME, PASSWORD)

# Upload the file
files = {"file": open(FILE_PATH, "rb")}
response = session.post(
    f"{CONFLUENCE_URL}/rest/api/content/{PAGE_ID}/child/attachment",
    files=files,
)

# Check the response status code
if response.status_code == 200:
    print("File uploaded successfully!")
else:
    print("File upload failed.")