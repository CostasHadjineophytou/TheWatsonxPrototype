import logging

class ModelManagement:
    # This is the class to manage the model info using the watsonx.ai API client created in account_info.py
    def __init__(self, watsonx):
        self.watsonx = watsonx

    def list_models(self):
        # This is the function to list all the models available..
        try:
            models = self.watsonx.foundation_models.get_model_specs()
            return models
        except Exception as e:
            logging.error(f"Error fetching models: {e}")
            raise RuntimeError("Error fetching models")

    def get_model_specs(self, model_id):
        # This is the function to get the model specs for a given model.
        try:
            model_specs = self.watsonx.foundation_models.get_model_specs(model_id=model_id)
            return model_specs
        except Exception as e:
            raise RuntimeError("Error fetching model specs")