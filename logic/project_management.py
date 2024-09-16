import json
from backend.authentication import Authentication
from backend.account_info import AccountInfo
import requests

auth = Authentication()
account_info = AccountInfo()

def fetch_and_save_projects_and_models():
    try:
        models = account_info.watsonx.foundation_models.get_model_specs()
        with open("models.json", "w") as f:
            json.dump(models, f)

        iam_token = auth.get_iam_token()
        projects = list_projects(iam_token)
        with open("user_projects.json", "w") as f:
            json.dump(projects, f)
    except Exception as e:
        print(f"Error: {e}")

def fetch_and_save_nlu_models():
    try:
        iam_token = auth.get_iam_token()
        nlu_models = list_nlu_models(iam_token)
        with open("nlu_models.json", "w") as f:
            json.dump(nlu_models, f)
    except Exception as e:
        print(f"Error: {e}")

def fetch_and_save_text_to_speech_voices():
    try:
        iam_token = auth.get_iam_token()
        tts_voices = list_text_to_speech_voices(iam_token)
        with open("text_to_speech_voices.json", "w") as f:
            json.dump(tts_voices, f)
    except Exception as e:
        print(f"Error: {e}")

def fetch_and_save_speech_to_text_models():
    try:
        iam_token = auth.get_iam_token()
        stt_models = list_speech_to_text_models(iam_token)
        with open("speech_to_text_models.json", "w") as f:
            json.dump(stt_models, f)
    except Exception as e:
        print(f"Error: {e}")

def fetch_and_save_all():
    fetch_and_save_projects_and_models()
    fetch_and_save_nlu_models()
    fetch_and_save_text_to_speech_voices()
    fetch_and_save_speech_to_text_models()

def get_projects():
    try:
        iam_token = auth.get_iam_token()
        projects = list_projects(iam_token)
        return [{"id": project["metadata"]["guid"], "name": project["entity"]["name"]} for project in projects]
    except Exception as e:
        print(f"Error: {e}")
        return []

def select_project(project_id: str):
    try:
        return {"status": "Project selected", "project_id": project_id}
    except Exception as e:
        print(f"Error: {e}")
        return {"status": "Error", "message": str(e)}

def list_projects(iam_token):
    headers = {
        "Authorization": f"Bearer {iam_token}",
        "Content-Type": "application/json"
    }
    endpoint = f"{account_info.projects_url}/v2/projects"
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        projects = response.json().get('resources', [])
        return projects
    else:
        error_message = f"Failed to list projects: {response.text}"
        raise RuntimeError(error_message)

def list_nlu_models(iam_token):
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Accept': 'application/json',
    }
    response = requests.get(f"{account_info.models_url}/v1/nlu_models", headers=headers)
    if response.status_code == 200:
        return response.json()['models']
    else:
        raise Exception(f"Failed to list NLU models: {response.text}")

def list_text_to_speech_voices(iam_token):
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Accept': 'application/json',
    }
    response = requests.get(f"{account_info.models_url}/v1/text_to_speech/voices", headers=headers)
    if response.status_code == 200:
        return response.json()['voices']
    else:
        raise Exception(f"Failed to list Text to Speech voices: {response.text}")

def list_speech_to_text_models(iam_token):
    headers = {
        'Authorization': f'Bearer {iam_token}',
        'Accept': 'application/json',
    }
    response = requests.get(f"{account_info.models_url}/v1/speech_to_text/models", headers=headers)
    if response.status_code == 200:
        return response.json()['models']
    else:
        raise Exception(f"Failed to list Speech to Text models: {response.text}")