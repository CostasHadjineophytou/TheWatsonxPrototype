import tkinter as tk

def create_params_tab(app):
    frame = tk.Frame(app.params_tab)
    frame.pack(padx=10, pady=10)

    # Temperature
    tk.Label(frame, text="Temperature:").grid(row=0, column=0, padx=5, pady=5)
    app.temperature_entry = tk.Entry(frame)
    app.temperature_entry.insert(0, "0.7")
    app.temperature_entry.grid(row=0, column=1, padx=5, pady=5)

    # Top P
    tk.Label(frame, text="Top P:").grid(row=1, column=0, padx=5, pady=5)
    app.top_p_entry = tk.Entry(frame)
    app.top_p_entry.insert(0, "1.0")
    app.top_p_entry.grid(row=1, column=1, padx=5, pady=5)

    # Top K
    tk.Label(frame, text="Top K:").grid(row=2, column=0, padx=5, pady=5)
    app.top_k_entry = tk.Entry(frame)
    app.top_k_entry.insert(0, "50")
    app.top_k_entry.grid(row=2, column=1, padx=5, pady=5)

    # Max New Tokens
    tk.Label(frame, text="Max New Tokens:").grid(row=3, column=0, padx=5, pady=5)
    app.max_new_tokens_entry = tk.Entry(frame)
    app.max_new_tokens_entry.insert(0, "1000")
    app.max_new_tokens_entry.grid(row=3, column=1, padx=5, pady=5)

    # Min New Tokens
    tk.Label(frame, text="Min New Tokens:").grid(row=4, column=0, padx=5, pady=5)
    app.min_new_tokens_entry = tk.Entry(frame)
    app.min_new_tokens_entry.insert(0, "1")
    app.min_new_tokens_entry.grid(row=4, column=1, padx=5, pady=5)

    # Repetition Penalty
    tk.Label(frame, text="Repetition Penalty:").grid(row=5, column=0, padx=5, pady=5)
    app.repetition_penalty_entry = tk.Entry(frame)
    app.repetition_penalty_entry.insert(0, "1.0")
    app.repetition_penalty_entry.grid(row=5, column=1, padx=5, pady=5)

    # Random Seed
    tk.Label(frame, text="Random Seed:").grid(row=6, column=0, padx=5, pady=5)
    app.random_seed_entry = tk.Entry(frame)
    app.random_seed_entry.insert(0, "42")
    app.random_seed_entry.grid(row=6, column=1, padx=5, pady=5)

    # Stop Sequences
    tk.Label(frame, text="Stop Sequences:").grid(row=7, column=0, sticky=tk.W)
    app.stop_sequences_entry = tk.Entry(frame)
    app.stop_sequences_entry.insert(0, "None")  # Default value set to 'None'
    app.stop_sequences_entry.grid(row=7, column=1)