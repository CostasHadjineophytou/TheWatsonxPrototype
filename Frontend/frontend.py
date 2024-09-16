import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import pandas as pd
from pathlib import Path
import os

from .env_pop_up import EnvPopUp

from .main_tab import create_main_tab
from .prompt_tuning_tab import create_prompt_tuning_tab
from .params_tab import create_params_tab
from .selection_tab import create_selection_tab
from .dataset_tab import create_dataset_tab
from .rag_tab import create_rag_tab
from .text_to_speech_tab import create_text_to_speech_tab, synthesize_text_ui
from .audio_to_text_tab import create_audio_to_text_tab, select_file, transcribe_audio_ui
from .nlu_tab import create_nlu_tab, analyze_text_ui, update_labels
from .chatbot_tab import create_chatbot_tab, send_message

from logic.project_management import (
    fetch_and_save_projects_and_models,
    get_projects,
    select_project
)
from logic.model_management import (
    get_models,
    select_model
)
from logic.dataset_management import (
    process_dataset,
    list_datasets
)
from logic.text_processing import (
    process_text,
    get_default_system_prompt,
    TextRequest
)

class AIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Islands Watson X Prototype")

         # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        # Settings menu so user can edit the API key and location
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu.add_command(label="API Key", command=self.edit_api_key)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)

        # Ensure JSON files are created if they do not exist
        if not Path("models.json").exists() or not Path("user_projects.json").exists():
            fetch_and_save_projects_and_models()

        # Load models and projects from JSON files
        self.models = self.load_json_from_file("models.json")
        self.projects = self.load_json_from_file("user_projects.json")

        # Fetch default system prompt
        self.default_system_prompt = get_default_system_prompt()["system_prompt"]

        # Fetch available datasets
        self.datasets = self.fetch_datasets()

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.prompt_tuning_tab = ttk.Frame(self.notebook)
        self.params_tab = ttk.Frame(self.notebook)
        self.selection_tab = ttk.Frame(self.notebook)
        self.dataset_tab = ttk.Frame(self.notebook)
        self.rag_tab = ttk.Frame(self.notebook)
        self.text_to_speech_tab = ttk.Frame(self.notebook)
        self.audio_to_text_tab = ttk.Frame(self.notebook)
        self.nlu_tab = ttk.Frame(self.notebook)
        self.chatbot_tab = ttk.Frame(self.notebook)
        # Add in all of the tabs from the imports!
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.prompt_tuning_tab, text="Prompt Tuning")
        self.notebook.add(self.params_tab, text="Parameters")
        self.notebook.add(self.selection_tab, text="Selection")
        self.notebook.add(self.dataset_tab, text="Data Processing")
        self.notebook.add(self.rag_tab, text="RAG")
        self.notebook.add(self.text_to_speech_tab, text="Text to Speech")
        self.notebook.add(self.audio_to_text_tab, text="Audio to Text")
        self.notebook.add(self.nlu_tab, text="NLU")
        self.notebook.add(self.chatbot_tab, text="Chatbot")

        # Main tab
        self.project_label = tk.Label(self.main_tab, text="Project: Not Selected")
        self.project_label.pack(pady=5)
        self.model_label = tk.Label(self.main_tab, text="Model: Not Selected")
        self.model_label.pack(pady=5)

        create_main_tab(self)

        create_prompt_tuning_tab(self)
        create_params_tab(self)
        create_selection_tab(self)
        create_dataset_tab(self)
        create_rag_tab(self)
        create_text_to_speech_tab(self)
        create_audio_to_text_tab(self)
        create_nlu_tab(self)
        create_chatbot_tab(self)

        # Check and create Dataset dir
        self.ensure_dataset_directory()

    def ensure_dataset_directory(self):
        dataset_dir = os.path.join(os.getcwd(), "Datasets")
        if not os.path.exists(dataset_dir):
            try:
                os.makedirs(dataset_dir)
                print(f"Created 'Datasets' directory at {dataset_dir}")
            except Exception as e:
                print(f"Error creating 'Datasets' directory: {str(e)}")
                messagebox.showerror("Error", f"Failed to create 'Datasets' directory: {str(e)}")
        else:
            print(f"'Datasets' directory already exists at {dataset_dir}")

    def load_json_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Error loading {filename} from file: {str(e)}")
            return []

    def fetch_datasets(self):
        datasets = list_datasets()
        return ["None"] + datasets["datasets"]

    def display_model_details(self, event):
        selected_index = self.model_listbox.curselection()
        if not selected_index:
            return
        selected_model = self.models['resources'][selected_index[0]]
        details = (
            f"Model ID: {selected_model.get('model_id')}\n"
            f"Label: {selected_model.get('label')}\n"
            f"Provider: {selected_model.get('provider')}\n"
            f"Source: {selected_model.get('source')}\n"
            f"Functions: {', '.join([func['id'] for func in selected_model.get('functions', [])])}\n"
            f"Short Description: {selected_model.get('short_description')}\n"
            f"Long Description: {selected_model.get('long_description')}\n"
            f"Input Tier: {selected_model.get('input_tier')}\n"
            f"Output Tier: {selected_model.get('output_tier')}\n"
            f"Number of Parameters: {selected_model.get('number_params')}\n"
            f"Min Shot Size: {selected_model.get('min_shot_size')}\n"
            f"Task IDs: {', '.join(selected_model.get('task_ids', []))}\n"
            f"Max Sequence Length: {selected_model.get('model_limits', {}).get('max_sequence_length')}\n"
            f"Lifecycle: {', '.join([lifecycle['id'] for lifecycle in selected_model.get('lifecycle', [])])}\n"
        )
        self.details_text.config(text=details)

    def update_main_tab_labels(self):
        selected_project_name = self.project_var.get()
        selected_project = next((project for project in self.projects if project['entity']['name'] == selected_project_name), None)
        selected_model_label = self.model_listbox.get(tk.ACTIVE)
        selected_model = next((model for model in self.models['resources'] if model['label'] == selected_model_label), None)

        # Update project label to show project name
        self.project_label.config(text=f"Project: {selected_project['entity']['name'] if selected_project else 'N/A'}")

        # Update model label to show model id
        self.model_label.config(text=f"Model: {selected_model['model_id'] if selected_model else 'N/A'}")

    def upload_dataset(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)
                preview = df.to_string(index=False)
                
                self.dataset_preview_text.delete(1.0, tk.END)
                self.dataset_preview_text.insert(tk.END, preview)
                self.dataset_preview_text.see("1.0")
                
                self.dataset_path = file_path
                messagebox.showinfo("Success", "Dataset loaded successfully")
            except Exception as e:
                self.dataset_preview_text.delete(1.0, tk.END)
                self.dataset_preview_text.insert(tk.END, f"Error loading dataset: {str(e)}")
                messagebox.showerror("Error", f"Failed to load dataset: {str(e)}")
        else:
            self.dataset_preview_text.delete(1.0, tk.END)
            self.dataset_preview_text.insert(tk.END, "No file selected")

        # Ensures the preview is updated
        self.dataset_preview_text.update_idletasks()

    def process_data(self):
        if not hasattr(self, 'dataset_path'):
            messagebox.showerror("Error", "Please upload a dataset first")
            return

        try:
            result = process_dataset(self.dataset_path)
            if result["message"] == "Dataset processed successfully":
                messagebox.showinfo("Success", "Dataset processed successfully")
                self.dataset_preview_text.delete(1.0, tk.END)  # Clear preview
                self.refresh_datasets()  # Refresh the datasets list so its now an option!
            else:
                messagebox.showerror("Error", result["message"])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process dataset: {str(e)}")

    def refresh_datasets(self):
        self.datasets = self.fetch_datasets()
        menu = self.rag_dataset_dropdown["menu"]
        menu.delete(0, "end")
        for dataset in self.datasets:
            menu.add_command(label=dataset, command=lambda value=dataset: self.rag_dataset_var.set(value))
        
        # Update the RAG preview for the currently selected dataset
        self.update_rag_preview(self.rag_dataset_var.get())

    def get_datasets_from_folder(self):
        datasets_dir = Path("Datasets")
        return [d.name for d in datasets_dir.iterdir() if d.is_dir()]

    def update_rag_preview(self, selected_dataset):
        if selected_dataset == "None":
            self.rag_preview_text.delete(1.0, tk.END)
            self.rag_preview_text.insert(tk.END, "No dataset selected")
            return

        try:
            dataset_path = Path("Datasets") / selected_dataset / f"{selected_dataset}.csv"
            if dataset_path.exists():
                df = pd.read_csv(dataset_path)
                preview = df.to_string(index=False)
                self.rag_preview_text.delete(1.0, tk.END)
                self.rag_preview_text.insert(tk.END, preview)
            else:
                self.rag_preview_text.delete(1.0, tk.END)
                self.rag_preview_text.insert(tk.END, f"Dataset file not found: {dataset_path}")
        except Exception as e:
            self.rag_preview_text.delete(1.0, tk.END)
            self.rag_preview_text.insert(tk.END, f"Error loading dataset: {str(e)}")

    def process_text(self):
        selected_project_name = self.project_var.get()
        selected_project = next((project for project in self.projects if project['entity']['name'] == selected_project_name), None)
        selected_model_label = self.model_listbox.get(tk.ACTIVE)
        selected_model = next((model for model in self.models['resources'] if model['label'] == selected_model_label), None)

        if not selected_project:
            messagebox.showwarning("Warning", "No project selected")
            return

        if not selected_model:
            messagebox.showwarning("Warning", "No model selected")
            return

        text = self.text_entry.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "No text entered")
            return

        stop_sequences = ["\nHuman:"]
        if self.stop_sequences_entry.get().strip():
            user_stop_sequences = [seq.strip() for seq in self.stop_sequences_entry.get().split(',') if seq.strip()]
            stop_sequences.extend(user_stop_sequences)
        stop_sequences = [seq for seq in stop_sequences if len(seq.encode('utf-8')) <= 240][:6]

        payload = {
            "text": text,
            "temperature": float(self.temperature_entry.get() or 1.0),
            "top_p": float(self.top_p_entry.get() or 1.0),
            "top_k": int(self.top_k_entry.get() or 50),
            "system_prompt": self.system_prompt_entry.get("1.0", tk.END).strip(),
            "example_conversation": self.example_conversation_entry.get("1.0", tk.END).strip(),
            "max_new_tokens": int(self.max_new_tokens_entry.get() or 1000),
            "min_new_tokens": int(self.min_new_tokens_entry.get() or 1),
            "repetition_penalty": float(self.repetition_penalty_entry.get() or 1.0),
            "random_seed": int(self.random_seed_entry.get() or 42),
            "stop_sequences": stop_sequences,  # Ensure it's always a list!
            "model_id": selected_model['model_id'],
            "project_id": selected_project['metadata']['guid'],
            "use_dataset": self.use_dataset_var.get(),
            "dataset_name": self.rag_dataset_var.get() if self.use_dataset_var.get() else None
        }

        request = TextRequest(**payload)
        result = process_text(request)
        if "result" in result:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result["result"])
            self.output_text.tag_add("monospace", "1.0", tk.END)
        else:
            messagebox.showerror("Error", "Failed to process text")
    
    def synthesize_text_ui(self):
        synthesize_text_ui(self)

    def select_file(self):
        select_file(self)

    def transcribe_audio_ui(self):
        transcribe_audio_ui(self)
    
    def analyze_text_ui(self):
        analyze_text_ui(self)

    def update_labels(self, result):
        update_labels(self, result)
    
    def send_message(self):
        send_message(self)

    def process_text_request(self, text):
        selected_project_name = self.project_var.get()
        selected_project = next((project for project in self.projects if project['entity']['name'] == selected_project_name), None)
        selected_model_label = self.model_listbox.get(tk.ACTIVE)
        selected_model = next((model for model in self.models['resources'] if model['label'] == selected_model_label), None)

        if not selected_project:
            messagebox.showwarning("Warning", "No project selected")
            return "No project selected"

        if not selected_model:
            messagebox.showwarning("Warning", "No model selected")
            return "No model selected"

        # Include chat history in the payload
        chat_history = self.chat_history.get("1.0", tk.END).strip()

        payload = {
            "text": text,
            "temperature": float(self.temperature_entry.get() or 1.0),
            "top_p": float(self.top_p_entry.get() or 1.0),
            "top_k": int(self.top_k_entry.get() or 50),
            "system_prompt": self.system_prompt_entry.get("1.0", tk.END).strip(),
            "example_conversation": chat_history,  # Use chat history as example conversation
            "max_new_tokens": int(self.max_new_tokens_entry.get() or 1000),
            "min_new_tokens": int(self.min_new_tokens_entry.get() or 1),
            "repetition_penalty": float(self.repetition_penalty_entry.get() or 1.0),
            "random_seed": int(self.random_seed_entry.get() or 42),
            "stop_sequences": ["\nHuman:"],
            "model_id": selected_model['model_id'],
            "project_id": selected_project['metadata']['guid'],
            "use_dataset": self.use_dataset_var.get(),
            "dataset_name": self.rag_dataset_var.get() if self.use_dataset_var.get() else None
        }

        request = TextRequest(**payload)
        result = process_text(request)
        return result.get("result", "Error processing text")

    def clear_chat_history(self):
            self.chat_history.config(state=tk.NORMAL)
            self.chat_history.delete("1.0", tk.END)
            self.chat_history.config(state=tk.DISABLED)
    
    def edit_api_key(self):
        EnvPopUp(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()