import tkinter as tk
from tkinter import messagebox, ttk
from logic.speech_services import synthesize_text, get_available_voices
import os

def create_text_to_speech_tab(app):
    text_label = tk.Label(app.text_to_speech_tab, text="Enter text to synthesize:")
    app.text_var = tk.StringVar()
    text_entry = tk.Entry(app.text_to_speech_tab, textvariable=app.text_var, width=50)
    
    voice_label = tk.Label(app.text_to_speech_tab, text="Voice:")
    app.voice_var = tk.StringVar()
    voices = get_available_voices()
    app.voice_dropdown = ttk.Combobox(app.text_to_speech_tab, textvariable=app.voice_var, values=voices, width=50)
    app.voice_dropdown.set('en-US_AllisonV3Voice')  # Default value
    
    accept_label = tk.Label(app.text_to_speech_tab, text="Accept:")
    app.accept_var = tk.StringVar(value='audio/wav')
    accept_entry = tk.Entry(app.text_to_speech_tab, textvariable=app.accept_var, width=50)
    
    pitch_label = tk.Label(app.text_to_speech_tab, text="Pitch (percentage):")
    app.pitch_var = tk.IntVar(value=0)
    pitch_slider = tk.Scale(app.text_to_speech_tab, variable=app.pitch_var, from_=-100, to=100, orient=tk.HORIZONTAL)
    
    speed_label = tk.Label(app.text_to_speech_tab, text="Speed (percentage):")
    app.speed_var = tk.IntVar(value=0)
    speed_slider = tk.Scale(app.text_to_speech_tab, variable=app.speed_var, from_=-100, to=100, orient=tk.HORIZONTAL)
    
    synthesize_button = tk.Button(app.text_to_speech_tab, text="Synthesize", command=app.synthesize_text_ui)
    
    # Layout UI elements
    text_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    text_entry.grid(row=0, column=1, padx=10, pady=10)
    voice_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    app.voice_dropdown.grid(row=1, column=1, padx=10, pady=10)
    accept_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    accept_entry.grid(row=2, column=1, padx=10, pady=10)
    pitch_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
    pitch_slider.grid(row=3, column=1, padx=10, pady=10)
    speed_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
    speed_slider.grid(row=4, column=1, padx=10, pady=10)
    synthesize_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

def synthesize_text_ui(app):
    text = app.text_var.get()
    voice = app.voice_var.get()
    accept = app.accept_var.get()
    pitch = app.pitch_var.get()
    speed = app.speed_var.get()
    
    if not text:
        messagebox.showwarning("No Text Entered", "Please enter some text first.")
        return

    audio_path = synthesize_text(text, voice, accept, pitch, speed)
    if audio_path:
        os.system(f"start {audio_path}")  # This plays audio file