from backend.model_management import ModelManagement
from backend.dataset_management import DatasetManagement
from backend.account_info import AccountInfo
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

SYSTEM_PROMPT = """You are Granite Chat, created by IBM. You're designed to assist with information and answer questions. You don't have feelings or emotions, so you don't experience happiness or sadness. You're here to help make the user's day more productive or enjoyable. Always respond in a helpful and informative manner. Provide a single, concise response to each query without continuing the conversation. Do not add 'Human:' or any other conversation continuation at the end of your response."""

class TextRequest:
    def __init__(self, text, temperature=0.7, top_p=1.0, top_k=50, system_prompt=SYSTEM_PROMPT, example_conversation="", max_new_tokens=1000, min_new_tokens=1, repetition_penalty=1.0, random_seed=42, stop_sequences=None, model_id="", project_id="", use_dataset=False, dataset_name=None):
        self.text = text
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.system_prompt = system_prompt
        self.example_conversation = example_conversation
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.repetition_penalty = repetition_penalty
        self.random_seed = random_seed
        self.stop_sequences = stop_sequences if stop_sequences is not None else []
        self.model_id = model_id
        self.project_id = project_id
        self.use_dataset = use_dataset
        self.dataset_name = dataset_name

def process_text(request: TextRequest):
    # This is the inference function for the text processing for the foundation models.
    try:
        account_info = AccountInfo()
        model_management = ModelManagement(account_info.watsonx)
        dataset_management = DatasetManagement()

        model_specs = model_management.get_model_specs(request.model_id)
        model = ModelInference(
            model_id=model_specs['model_id'],
            credentials=account_info.credentials,
            project_id=request.project_id
        )
        
        full_prompt = ""
        if request.system_prompt:
            full_prompt += f"{request.system_prompt}\n\n"
        if request.example_conversation:
            full_prompt += f"{request.example_conversation}\n\n"
        
        # For RAG
        if request.use_dataset:
            dataset_name = request.dataset_name
            relevant_entries = dataset_management.find_relevant_entries(request.text, dataset_name)
            if relevant_entries:
                full_prompt += "Relevant information:\n"
                for entry in relevant_entries:
                    full_prompt += f"- {entry}\n"
                full_prompt += "\n"
        
        full_prompt += f"Human: {request.text}\n\nAI:"
        
        params = {
            GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
            GenParams.TEMPERATURE: request.temperature,
            GenParams.TOP_K: request.top_k,
            GenParams.TOP_P: request.top_p,
            GenParams.MAX_NEW_TOKENS: request.max_new_tokens,
            GenParams.MIN_NEW_TOKENS: request.min_new_tokens,
            GenParams.REPETITION_PENALTY: request.repetition_penalty,
            GenParams.RANDOM_SEED: request.random_seed,
            GenParams.STOP_SEQUENCES: request.stop_sequences
        }
        
        result = model.generate_text(prompt=full_prompt, params=params)
        
        for stop_seq in request.stop_sequences:
            if stop_seq in result:
                result = result.split(stop_seq)[0]
        
        return {"result": result.strip()}

    except Exception as e:
        print(f"Error: {e}")
        return {"result": str(e)}

def get_default_system_prompt():
    return {"system_prompt": SYSTEM_PROMPT}