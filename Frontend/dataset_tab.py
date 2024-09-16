import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import pandas as pd

def create_dataset_tab(app):
    app.upload_button = tk.Button(app.dataset_tab, text="Upload Dataset", command=app.upload_dataset)
    app.upload_button.pack(pady=10)

    app.dataset_preview_frame = ttk.Frame(app.dataset_tab)
    app.dataset_preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    app.dataset_preview_text = tk.Text(app.dataset_preview_frame, height=20, width=80, wrap=tk.NONE)
    app.dataset_preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    app.dataset_preview_v_scrollbar = ttk.Scrollbar(app.dataset_preview_frame, orient="vertical", command=app.dataset_preview_text.yview)
    app.dataset_preview_v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.dataset_preview_h_scrollbar = ttk.Scrollbar(app.dataset_tab, orient="horizontal", command=app.dataset_preview_text.xview)
    app.dataset_preview_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    app.dataset_preview_text.configure(yscrollcommand=app.dataset_preview_v_scrollbar.set, xscrollcommand=app.dataset_preview_h_scrollbar.set)

    app.process_button = tk.Button(app.dataset_tab, text="Process Data", command=app.process_data)
    app.process_button.pack(pady=10)