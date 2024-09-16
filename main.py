import os
from dotenv import load_dotenv

load_dotenv()

import tkinter as tk
from Frontend.frontend import AIApp
from logic.project_management import fetch_and_save_all

def start_frontend():
    root = tk.Tk()
    app = AIApp(root)
    root.mainloop()
    fetch_and_save_all()

if __name__ == "__main__":
    # Start the frontend application
    start_frontend()