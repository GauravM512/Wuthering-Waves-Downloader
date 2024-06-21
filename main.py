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

    print("Selected folder:", folder_path)
    
    # Assuming download.start_download takes a path as an argument
    download.start_download(folder_path)

