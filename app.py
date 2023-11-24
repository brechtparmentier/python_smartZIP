import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Style

IGNORE_LIST = ["node_modules", "__pycache__", ".git", ".vscode", ".idea", ".zip"]

# Voeg de FOLDER_PATH variabele toe
FOLDER_PATH = (
    None  # U kunt hier een standaardpad instellen, of None laten om de GUI te gebruiken
)

root = tk.Tk()  # Definieer root als een globale variabele


def should_ignore(path):
    return any(ignore_item in path for ignore_item in IGNORE_LIST)


def add_folder_to_zip(zipf, folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_path)
            zipf.write(file_path, arcname)


def compress_folders():
    global FOLDER_PATH  # Gebruik de globale FOLDER_PATH variabele
    folder_path = FOLDER_PATH or filedialog.askdirectory(
        title="Selecteer een map om te comprimeren", initialdir=os.getcwd()
    )

    if folder_path and not should_ignore(folder_path):
        default_name = os.path.basename(folder_path)
        zip_filename = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".zip",
            filetypes=[("ZIP-bestanden", "*.zip")],
        )

        if zip_filename:
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                add_folder_to_zip(zipf, folder_path)
            messagebox.showinfo("Succes", f"Map is gecomprimeerd naar {zip_filename}")


def init_gui():
    global root  # Gebruik de globale root variabele
    root.title("Mapcompressor")
    style = Style()
    style.theme_use("clam")
    Button(root, text="Comprimeer Map", command=compress_folders).pack(pady=20)
    root.mainloop()


if __name__ == "__main__":
    init_gui()
