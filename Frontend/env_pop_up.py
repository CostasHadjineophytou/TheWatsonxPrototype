import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

class EnvPopUp:
    def __init__(self, parent):
        self.parent = parent
        self.top = tk.Toplevel(parent)
        self.top.title("Edit API Key and Location")

        # API Key
        tk.Label(self.top, text="API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.api_key_entry = tk.Entry(self.top, show='*', width=50)
        self.api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Location
        tk.Label(self.top, text="Location:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.location_var = tk.StringVar(self.top)
        self.location_var.set("eu-gb")  # Default value
        self.location_dropdown = tk.OptionMenu(self.top, self.location_var, "eu-gb", "us-south", "au-syd", "jp-tok")
        self.location_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Save button
        tk.Button(self.top, text="Save", command=self.save).grid(row=2, columnspan=2, pady=10)

    def save(self):
        api_key = self.api_key_entry.get().strip()
        location = self.location_var.get().strip()

        if api_key and location:
            self.update_env_file("IBM_CLOUD_API_KEY", api_key)
            self.update_env_file("IBM_CLOUD_MODELS_URL", f"https://{location}.ml.cloud.ibm.com")
            self.update_env_file("IBM_CLOUD_PROJECTS_URL", f"https://api.{location}.dataplatform.cloud.ibm.com")
            messagebox.showinfo("Info", "API Key and URLs updated successfully")
            self.top.destroy()
        else:
            messagebox.showwarning("Warning", "Please enter both API Key and Location")

    def update_env_file(self, key, value):
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, "r") as file:
                lines = file.readlines()
            with open(env_path, "w") as file:
                for line in lines:
                    if line.startswith(key):
                        file.write(f"{key}={value}\n")
                    else:
                        file.write(line)
        else:
            with open(env_path, "w") as file:
                file.write(f"{key}={value}\n")