# Student File Management Portal
This is a web application that allows students to connect to their Dropbox account and manage their files. The application is built using Python and Django, and it uses the Dropbox API v2 to access and modify files on the Dropbox platform.

# System Requirements
To run this application, you will need:
 • Python 3
 • Django
 • Dropbox Python SDK

# Setup
1. Clone this repository to your local machine.
2. Create and activate a virtual environment by running python3 -m venv myenv    and activate it.
3. Install the required dependencies by running pip install -r       requirements.txt.
4. Start the development server by running python3 manage.py runserver.

# Features
 • Connect to your Dropbox account by authorizing the app.
 • View all your files and folders on Dropbox.
 • Delete, download, search and upload files.
 • Filter files by file type.
 
 
# Limitations and Known Issues

 • There may be some bugs or issues that have not been discovered yet.

# Dependencies
This project depends on the following libraries:
 • Dropbox Python SDK
 • Django

# Challenges Faced
During the development of this project, I faced a challenge that I had to overcome:

 • Handling OAuth2 Authorization Flow: The most significant challenge I faced was implementing the Dropbox OAuth2 Authorization Flow using the DropboxOAuth2Flow function provided by the python SDK. After reading through the documentation and some experimentation, I was able to use the Dropbox OAuth2 API directly by using HTTP requests and handling the responses.
