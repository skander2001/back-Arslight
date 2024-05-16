


from gtts import gTTS
from IPython.display import Audio
import tkinter as tk
from tkinter import ttk
from datetime import datetime

language=["en", "ar"]
date = datetime.now().strftime("%d%m%Y")

def speech():
    text = text_entry.get()
    language = language_dropdown.get()
    gTTS_object = gTTS(text=text, lang=language, slow=False)
    filename = f"gtts_{date}.wav"
    gTTS_object.save(filename)
    status_label.config(text=f"Speech saved to {filename}")

# Create main window
root = tk.Tk()
root.title("Text-to-Speech Converter")

# Text input
text_label = tk.Label(root, text="Enter text:")
text_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
text_entry = tk.Entry(root, width=40)
text_entry.grid(row=0, column=1, padx=10, pady=5)

# Language selection
language_label = tk.Label(root, text="Select language:")
language_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
languages = ['en', 'ar', 'fr']  # Example languages
language_dropdown = ttk.Combobox(root, values=languages, width=37)
language_dropdown.current(0)  # Set default language
language_dropdown.grid(row=1, column=1, padx=10, pady=5)

# Button to generate speech
generate_button = tk.Button(root, text="Generate Speech", command=speech)
generate_button.grid(row=2, columnspan=2, padx=10, pady=10)

# Status label
status_label = tk.Label(root, text="")
status_label.grid(row=3, columnspan=2)

# Run the GUI
root.mainloop()