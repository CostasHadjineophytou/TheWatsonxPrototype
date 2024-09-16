import tkinter as tk
from tkinter import filedialog, messagebox
from logic.speech_services import transcribe_audio

def create_audio_to_text_tab(app):
    file_label = tk.Label(app.audio_to_text_tab, text="Select an audio file:")
    app.file_path_var = tk.StringVar()
    file_entry = tk.Entry(app.audio_to_text_tab, textvariable=app.file_path_var, width=50)
    file_button = tk.Button(app.audio_to_text_tab, text="Browse", command=app.select_file)
    transcribe_button = tk.Button(app.audio_to_text_tab, text="Transcribe", command=app.transcribe_audio_ui)
    result_label = tk.Label(app.audio_to_text_tab, text="Transcription:")
    result_text = tk.Text(app.audio_to_text_tab, height=20, width=80)
    
    def set_result_var():
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, app.result_var.get())

    app.result_var = tk.StringVar()
    app.result_var.trace("w", lambda *args: set_result_var())

    file_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    file_entry.grid(row=0, column=1, padx=10, pady=10)
    file_button.grid(row=0, column=2, padx=10, pady=10)
    transcribe_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    result_label.grid(row=2, column=0, padx=10, pady=10, sticky="ne")
    result_text.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

def select_file(app):
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.ogg *.m4a *.wma")]
    )
    if file_path:
        app.file_path_var.set(file_path)

def transcribe_audio_ui(app):
    file_path = app.file_path_var.get()
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select an audio file first.")
        return

    transcription = transcribe_audio(file_path)
    if transcription:
        app.result_var.set(transcription)
    else:
        messagebox.showerror("Transcription Failed", "Error occurred during transcription.")