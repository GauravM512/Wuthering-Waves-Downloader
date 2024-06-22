import download
import tkinter as tk
from tkinter import filedialog
import json
import os

config_path = "config.json"
default_config = {
    "threads": 4,
    "path": ""
}

if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = json.load(f)
else:
    with open(config_path, "w") as f:
        json.dump(default_config, f, indent=4)
    config = default_config

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    root.destroy()  # Close the Tkinter window
    return folder_path

if __name__ == "__main__":
    if config.get("path", "") == "":
        print("Please select a folder to download the files to.")
        folder_path = select_folder()
        config["path"] = folder_path
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
    else:
        folder_path = config["path"]


    print("1. Install game")
    print("2. Verify game")
    choice = input("Enter your choice: ")
    while choice not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter your choice: ")
    if choice == "1":
        print("Selected folder:", folder_path)
        
        download.start_download(folder_path)
    else:
        print("Selected folder:", folder_path)
        print("Verifying game...")
        download.verify_game(folder_path)
