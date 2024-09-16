import logging
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from backend.account_info import AccountInfo

class NLUService:
    def __init__(self, account_info):
        self.account_info = account_info

    def init_nlu_service(self):
        # This is the function to initialise the Natural Language Understanding service.
        try:
            iam_token = self.account_info.get_iam_token()
            credentials = self.account_info.get_service_credentials(iam_token, "Natural Language Understanding")
            if credentials:
                authenticator = IAMAuthenticator(credentials['apikey'])
                nlu = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
                nlu.set_service_url(credentials['url'])
                return nlu
            else:
                raise Exception("Failed to retrieve or create service credentials.")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def analyze_text(self, text, analysis_type, nlu):
        # This is the function to inference the NLU.
        if nlu is None:
            print("Error: Natural Language Understanding service is not initialised.")
            return None

        features = {analysis_type: {}}
        if analysis_type == 'all':
            features = {
                'sentiment': {},
                'emotion': {},
                'entities': {},
                'keywords': {},
                'categories': {},
                'concepts': {},
                'relations': {},
                'semantic_roles': {}
            }
        try:
            response = nlu.analyze(
                text=text,
                features=features
            ).get_result()
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None