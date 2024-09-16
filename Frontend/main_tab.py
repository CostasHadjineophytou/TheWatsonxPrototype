import tkinter as tk

def create_main_tab(app):
    # Create a frame for the text entry and process button
    app.action_frame = tk.Frame(app.main_tab)
    app.action_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    app.text_entry = tk.Text(app.action_frame, width=50, height=3)
    app.text_entry.pack(pady=5)

    # Process button
    app.process_text_button = tk.Button(app.action_frame, text="Process Text", command=app.process_text)
    app.process_text_button.pack(pady=5)

    # Create a frame for the output
    app.output_frame = tk.Frame(app.main_tab, bd=2, relief=tk.SUNKEN)
    app.output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    app.output_label = tk.Label(app.output_frame, text="Output", font=("Arial", 12, "bold"))
    app.output_label.pack(pady=5)

    app.output_text = tk.Text(app.output_frame, width=50, height=20, wrap=tk.WORD)
    app.output_text.pack(pady=5, fill=tk.BOTH, expand=True)

    app.output_scrollbar = tk.Scrollbar(app.output_frame, command=app.output_text.yview)
    app.output_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.output_text.config(yscrollcommand=app.output_scrollbar.set)