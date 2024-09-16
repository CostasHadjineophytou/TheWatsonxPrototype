import os
from ibm_watsonx_ai import APIClient, Credentials
from backend.authentication import Authentication
from backend.resource_service import ResourceService

class AccountInfo:
    def __init__(self):
        # Load the API key from the .env file
        self.api_key = os.getenv('IBM_CLOUD_API_KEY')
        self.projects_url = os.getenv('IBM_CLOUD_PROJECTS_URL')
        self.models_url = os.getenv('IBM_CLOUD_MODELS_URL')
        # create credentials object using the API key & models url
        self.credentials = Credentials(
            url=self.models_url,
            api_key=self.api_key
        )
        # create APIClient object using the credentials (this is for watsonx model information)
        self.watsonx = APIClient(self.credentials)
        # create authentication object
        self.auth = Authentication()
        # create resource service object
        self.resource_service = ResourceService()

        if not self.api_key or not self.projects_url or not self.models_url:
            raise ValueError("API key or URLs are not set in the environment variables.")

    # Localise the IAM token to Account Info class
    def get_iam_token(self):
        return self.auth.get_iam_token()

    # Localise the service credentials to Account Info class
    def get_service_credentials(self, iam_token, service_name):
        return self.resource_service.get_service_credentials(iam_token, service_name)