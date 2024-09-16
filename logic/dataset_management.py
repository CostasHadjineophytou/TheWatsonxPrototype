from backend.dataset_management import DatasetManagement

dataset_management = DatasetManagement()

def process_dataset(file_path: str):
    return dataset_management.process_dataset(file_path)

def list_datasets():
    return dataset_management.list_datasets()

def find_relevant_entries(query, dataset_name, top_k=3):
    return dataset_management.find_relevant_entries(query, dataset_name, top_k)