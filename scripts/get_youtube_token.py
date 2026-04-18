"""Helper to perform console-based OAuth for YouTube and save token file.

Run this locally, follow the instructions, and paste the code when prompted.
It will save credentials to `data/youtube_token.json`.
"""
import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
SECRETS_PATH = BASE_DIR / 'client_secrets.json'
TOKEN_PATH = BASE_DIR / 'data' / 'youtube_token.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube']

def run_console_flow():
    if not SECRETS_PATH.exists():
        print(f"ERROR: {SECRETS_PATH} not found. Place your client_secrets.json in the project root.")
        return

    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_PATH), SCOPES)
    creds = flow.run_console()

    os.makedirs(TOKEN_PATH.parent, exist_ok=True)
    with open(TOKEN_PATH, 'w') as f:
        f.write(creds.to_json())

    print(f"Saved credentials to: {TOKEN_PATH}")

if __name__ == '__main__':
    run_console_flow()
