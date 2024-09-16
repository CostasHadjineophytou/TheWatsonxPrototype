import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

class DatasetManagement:
    def process_dataset(self, file_path: str):
        # This is the function to process the dataset and create the necessary files for RAG search.
        try:
            filename = Path(file_path).stem
            dataset_dir = Path("Datasets") / filename
            dataset_dir.mkdir(parents=True, exist_ok=True)

            df = pd.read_csv(file_path)
            
            texts = df.apply(lambda row: ' '.join([f"{col}: {val}" for col, val in row.items()]), axis=1).tolist()

            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts, show_progress_bar=True)
            faiss.normalize_L2(embeddings)

            index = faiss.IndexFlatIP(embeddings.shape[1])
            index.add(embeddings)

            faiss_index_path = dataset_dir / f"{filename}_faiss_index.bin"
            faiss.write_index(index, str(faiss_index_path))

            pickle_path = dataset_dir / f"{filename}.pkl"
            df.to_pickle(pickle_path)

            csv_path = dataset_dir / f"{filename}.csv"
            df.to_csv(csv_path, index=False)

            return {"message": "Dataset processed successfully"}

        except Exception as e:
            print(f"Error: {e}")
            return {"message": "Error processing dataset"}

    def list_datasets(self):
        try:
            datasets_dir = Path("Datasets")
            datasets = [d.name for d in datasets_dir.iterdir() if d.is_dir()]
            return {"datasets": datasets}
        except Exception as e:
            print(f"Error: {e}")
            return {"datasets": []}

    def find_relevant_entries(self, query, dataset_name, top_k=3):
        # This is the RAG search function, with a limit of top 3 relevant results only.
        dataset_dir = Path("Datasets") / dataset_name
        faiss_index_path = dataset_dir / f"{dataset_name}_faiss_index.bin"
        pickle_path = dataset_dir / f"{dataset_name}.pkl"

        if not faiss_index_path.exists() or not pickle_path.exists():
            return []

        index = faiss.read_index(str(faiss_index_path))
        model = SentenceTransformer('all-MiniLM-L6-v2')
        original_data = pd.read_pickle(pickle_path)

        query_vector = model.encode([query])
        faiss.normalize_L2(query_vector)
        _, I = index.search(query_vector, top_k)
        
        relevant_entries = original_data.iloc[I[0]].to_dict('records')
        return [self.format_entry(entry) for entry in relevant_entries]

    def format_entry(self, entry):
        return ', '.join([f"{key}: {value}" for key, value in entry.items()])