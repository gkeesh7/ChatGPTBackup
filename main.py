import openai_secret_manager
import openai
import os
import datetime
import requests
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

openai.api_key = os.getenv("OPENAI_API_KEY")

# Authenticate with Google Drive API
assert "google" in openai_secret_manager.get_services()
secrets = openai_secret_manager.get_secret("google")
creds = Credentials.from_authorized_user_info(info=secrets)
service = build("drive", "v3", credentials=creds)

# Find the reference document
query = "name='Reference Doc' and mimeType='application/vnd.google-apps.document'"
result = service.files().list(q=query).execute()
reference_doc_id = result['files'][0]['id']

# Get the chat history from OpenAI
response = openai.Completion.create(
  engine="davinci",
  prompt=(
      "Get the chat history from ChatGPT:\n"
      "Date: 2023-05-10"
  ),
  temperature=0.5,
  max_tokens=1024,
  n=1,
  stop=None,
  timeout=60,
)
chat_history = response.choices[0].text

# Append the chat history to the end of the reference document
requests.post(
    f"https://docs.google.com/document/d/{reference_doc_id}/edit",
    headers={"Authorization": f"Bearer {creds.token}"},
    params={"id": reference_doc_id, "append": "true"},
    data=chat_history.encode("utf-8")
)

print("Chat history copied and appended to the end of Reference Doc!")
