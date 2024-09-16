import tkinter as tk

def create_chatbot_tab(app):
    # Create a frame for the chat history
    app.chat_frame = tk.Frame(app.chatbot_tab, bd=2, relief=tk.SUNKEN)
    app.chat_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    app.chat_history = tk.Text(app.chat_frame, width=50, height=20, wrap=tk.WORD, state=tk.DISABLED)
    app.chat_history.pack(pady=5, fill=tk.BOTH, expand=True)

    app.chat_scrollbar = tk.Scrollbar(app.chat_frame, command=app.chat_history.yview)
    app.chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.chat_history.config(yscrollcommand=app.chat_scrollbar.set)

    # Add text tags for user and bot messages
    app.chat_history.tag_configure("user", foreground="black")
    app.chat_history.tag_configure("bot", foreground="blue")

    # Create a frame for the input and send button
    app.input_frame = tk.Frame(app.chatbot_tab)
    app.input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

    app.input_entry = tk.Text(app.input_frame, width=50, height=3)
    app.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5, padx=5)

    app.send_button = tk.Button(app.input_frame, text="Send", command=app.send_message)
    app.send_button.pack(side=tk.RIGHT, pady=5, padx=5)

    # Create a frame for the clear history button
    app.clear_history_button = tk.Button(app.input_frame, text="Clear History", command=app.clear_chat_history)
    app.clear_history_button.pack(side=tk.RIGHT, pady=5, padx=5)

def send_message(app):
    user_message = app.input_entry.get("1.0", "end-1c").strip()
    if user_message:
        app.input_entry.delete("1.0", tk.END)
        app.chat_history.config(state=tk.NORMAL)
        app.chat_history.insert(tk.END, f"You: {user_message}\n", "user")
        app.chat_history.config(state=tk.DISABLED)
        app.chat_history.yview(tk.END)
        
        response = app.process_text_request(user_message)
        
        app.chat_history.config(state=tk.NORMAL)
        app.chat_history.insert(tk.END, f"Bot: {response}\n", "bot")
        app.chat_history.config(state=tk.DISABLED)
        app.chat_history.yview(tk.END)

def clear_chat_history(app):
    app.chat_history.config(state=tk.NORMAL)
    app.chat_history.delete("1.0", tk.END)
    app.chat_history.config(state=tk.DISABLED)