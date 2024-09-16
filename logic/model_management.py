from backend.account_info import AccountInfo
from backend.model_management import ModelManagement

account_info = AccountInfo()
model_management = ModelManagement(account_info.watsonx)

def get_models(project_id: str):
    try:
        models = model_management.list_models()
        return models
    except Exception as e:
        print(f"Error: {e}")
        return []

def select_model(model_id: str):
    try:
        model_specs = model_management.get_model_specs(model_id)
        return {"status": "Model selected", "model_specs": model_specs}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Error", "message": str(e)}