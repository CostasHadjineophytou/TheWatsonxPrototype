import tkinter as tk

def create_selection_tab(app):
    # Project selection
    tk.Label(app.selection_tab, text="Select Project:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    app.project_var = tk.StringVar(app.selection_tab)
    project_names = [project['entity']['name'] for project in app.projects if 'entity' in project and 'name' in project['entity']]
    if project_names:
        app.project_var.set(project_names[0])  # Seta default value
    app.project_dropdown = tk.OptionMenu(app.selection_tab, app.project_var, *project_names)
    app.project_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    # Model selection
    tk.Label(app.selection_tab, text="Select Model:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    app.model_listbox = tk.Listbox(app.selection_tab, width=50, height=20)
    app.model_listbox.grid(row=1, column=1, rowspan=2, padx=10, pady=5, sticky="nsew")
    app.model_listbox.bind('<<ListboxSelect>>', app.display_model_details)
    for model in app.models['resources']:
        if isinstance(model, dict) and 'model_id' in model:
            app.model_listbox.insert(tk.END, model['label'])  # Display model label

    app.select_model_button = tk.Button(app.selection_tab, text="Select Model", command=app.update_main_tab_labels)
    app.select_model_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Model details
    app.details_frame = tk.Frame(app.selection_tab, bd=2, relief=tk.SUNKEN)
    app.details_frame.grid(row=1, column=2, rowspan=3, padx=10, pady=5, sticky="nsew")
    app.details_label = tk.Label(app.details_frame, text="Model Information", font=("Arial", 12, "bold"))
    app.details_label.pack(pady=5)
    app.details_text = tk.Label(app.details_frame, width=50, height=20, anchor="nw", justify="left", bd=1, relief=tk.SUNKEN, wraplength=300)
    app.details_text.pack(pady=5, fill=tk.BOTH, expand=True)

    # Configure grid weights
    app.selection_tab.grid_columnconfigure(1, weight=1)
    app.selection_tab.grid_columnconfigure(2, weight=1)
    app.selection_tab.grid_rowconfigure(1, weight=1)
    app.selection_tab.grid_rowconfigure(2, weight=1)
    app.selection_tab.grid_rowconfigure(3, weight=1)