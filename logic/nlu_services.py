from backend.nlu_services import NLUService
from backend.account_info import AccountInfo

account_info = AccountInfo()
nlu_service = NLUService(account_info)

def analyze_text(text, analysis_type):
    nlu = nlu_service.init_nlu_service()
    if nlu is None:
        print("Error: Natural Language Understanding service initialisation failed.")
        return None
    return nlu_service.analyze_text(text, analysis_type, nlu)