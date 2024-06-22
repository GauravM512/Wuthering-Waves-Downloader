import download
import tkinter as tk
from tkinter import filedialog
import json
import os

# Configuration file path and default settings
CONFIG_PATH = "config.json"
DEFAULT_CONFIG = {
    "threads": 4,
    "path": "",
}





def load_config(config_path, default_config):
    """
    Load the configuration from the config file if it exists.
    Otherwise, create the file with default settings.
    """
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    else:
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config

def select_folder():
    """
    Open a file dialog for the user to select a folder.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folder_path = filedialog.askdirectory()
    root.destroy()  # Close the Tkinter window
    return folder_path

def main():
    config = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    
    if not config.get("path"):
        print("Please select a folder to download the files to.")
        folder_path = select_folder()
        if folder_path:  # Check if a folder was selected
            config["path"] = folder_path
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)
        else:
            print("No folder selected. Exiting...")
            return
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
        download.start_download(folder_path, threads=config["threads"])
        print("Game installed successfully.")
        print("Opening game folder...")
        os.startfile(os.path.join(folder_path, "Client/Binaries/Win64/"))
        print("Run Client-Win64-Shipping.exe to start the game")
    else:
        print("Selected folder:", folder_path)
        print("Verifying game...")
        download.verify_game(folder_path)
        print("Game verified successfully.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...") # Handle Ctrl+C
        quit(0)
