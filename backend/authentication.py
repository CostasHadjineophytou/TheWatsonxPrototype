import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

class Authentication:
    def __init__(self):
        self.api_key = os.getenv('IBM_CLOUD_API_KEY')
        if not self.api_key:
            raise ValueError("API key is not set in the environment variables.")

    # Get the IAM token function - relies on the API key being set in the environment variables.
    def get_iam_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
        data = {
            'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
            'apikey': self.api_key,
        }
        response = requests.post(IAM_TOKEN_URL, headers=headers, data=data)
        if response.status_code == 200:
            token = response.json()['access_token']
            logging.info("IAM token retrieved successfully")
            return token
        else:
            error_message = f"Failed to get IAM token: {response.text}"
            raise RuntimeError(error_message)