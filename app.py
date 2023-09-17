import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Style

import zipfile
import os

# Functie om mappen te selecteren en te comprimeren
def compress_folders():
    folder_paths = filedialog.askopenfilenames(
        title="Selecteer mappen om te comprimeren",
        filetypes=(("Mappen", ""), ("Alle bestanden", "*.*")),
        initialdir="/",  # Stel het beginpad in op /
    )

    if folder_paths:
        zip_filename = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP-bestanden", "*.zip")]
        )

        if zip_filename:
            # Voeg de bestanden toe aan het ZIP-bestand
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for folder_path in folder_paths:
                    if not should_ignore(folder_path):
                        add_folder_to_zip(zipf, folder_path)

            messagebox.showinfo("Succes", f"{len(folder_paths)} mappen zijn gecomprimeerd naar {zip_filename}")

# Functie om mappen toe te voegen aan het ZIP-bestand
def add_folder_to_zip(zipf, folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_path)
            zipf.write(file_path, arcname)

# Functie om te controleren of een pad moet worden genegeerd
def should_ignore(path):
    ignore_list = [
        "node_modules",  # Negeer node_modules-map
        "__pycache__",   # Negeer __pycache__-map
        ".git",          # Negeer .git-map
        ".vscode",       # Negeer .vscode-map
        ".idea",         # Negeer .idea-map
        ".zip",          # Negeer .zip-bestanden
    ]

    return any(ignore_item in path for ignore_item in ignore_list)

# GUI-initialisatie
root = tk.Tk()
root.title("Mapcompressor")

# Geef de GUI een modern thema
style = Style()
style.theme_use("clam")

# Maak een knop met een modern uiterlijk
compress_button = Button(root, text="Comprimeer Mappen", command=compress_folders)
compress_button.pack(pady=20)

root.mainloop()
