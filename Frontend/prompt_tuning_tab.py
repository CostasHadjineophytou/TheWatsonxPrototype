import tkinter as tk

def create_prompt_tuning_tab(app):
    # System Prompt
    tk.Label(app.prompt_tuning_tab, text="System Prompt:").pack(pady=5)
    app.system_prompt_entry = tk.Text(app.prompt_tuning_tab, height=5, width=50)
    app.system_prompt_entry.insert(tk.END, app.default_system_prompt)
    app.system_prompt_entry.pack(pady=5)

    # Example Conversation
    tk.Label(app.prompt_tuning_tab, text="Example Conversation:").pack(pady=5)
    app.example_conversation_entry = tk.Text(app.prompt_tuning_tab, height=10, width=50)
    app.example_conversation_entry.pack(pady=5)