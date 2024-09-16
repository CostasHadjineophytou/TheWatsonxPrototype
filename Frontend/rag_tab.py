import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pathlib import Path
import pandas as pd

def create_rag_tab(app):
    # Dataset selection dropdown
    tk.Label(app.rag_tab, text="Select Dataset:").pack(pady=5)
    app.rag_dataset_var = tk.StringVar(app.rag_tab)
    app.rag_dataset_var.set("None")  # Default value
    app.rag_datasets = app.get_datasets_from_folder()
    app.rag_dataset_dropdown = tk.OptionMenu(app.rag_tab, app.rag_dataset_var, "None", *app.rag_datasets)
    app.rag_dataset_dropdown.pack(pady=5)

    # Checkbox to use dataset
    app.use_dataset_var = tk.BooleanVar()
    app.use_dataset_checkbox = tk.Checkbutton(app.rag_tab, text="Use Dataset", variable=app.use_dataset_var)
    app.use_dataset_checkbox.pack(pady=5)

    # Create a frame for the preview and add elements
    app.rag_preview_frame = ttk.Frame(app.rag_tab)
    app.rag_preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    tk.Label(app.rag_preview_frame, text="Dataset Preview:").pack(pady=5)
    app.rag_preview_text = tk.Text(app.rag_preview_frame, height=20, width=80, wrap=tk.NONE)
    app.rag_preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    app.rag_preview_v_scrollbar = ttk.Scrollbar(app.rag_preview_frame, orient="vertical", command=app.rag_preview_text.yview)
    app.rag_preview_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.rag_preview_h_scrollbar = ttk.Scrollbar(app.rag_tab, orient="horizontal", command=app.rag_preview_text.xview)
    app.rag_preview_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    app.rag_preview_text.configure(yscrollcommand=app.rag_preview_v_scrollbar.set, xscrollcommand=app.rag_preview_h_scrollbar.set)
    app.rag_dataset_var.trace('w', lambda *args: app.update_rag_preview(app.rag_dataset_var.get()))