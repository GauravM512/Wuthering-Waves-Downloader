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
    "GAME": "",
}

def load_config(config_path: str, default_config: dict) -> dict:
    """
    Load the configuration from the config file if it exists.
    Otherwise, create the file with default settings.

    Args:
        config_path (str): The path to the configuration file.
        default_config (dict): The default configuration settings.

    Returns:
        dict: The loaded or default configuration settings.
    """
    try:
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)
        else:
            with open(config_path, "w") as f:
                json.dump(default_config, f, indent=4)
            return default_config
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading config: {e}")
        return default_config

def select_folder() -> str:
    """
    Open a file dialog for the user to select a folder.

    Returns:
        str: The selected folder path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

def update_config(config: dict, key: str, value: str) -> None:
    """
    Update the configuration file with a new value.

    Args:
        config (dict): The current configuration.
        key (str): The key to update.
        value (str): The new value.
    """
    config[key] = value
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def select_game_version(config: dict) -> None:
    """
    Prompt the user to select a game version and update the configuration.

    Args:
        config (dict): The current configuration.
    """
    print("1. Googleplay")
    print("2. Overseas")
    choice = input("Enter your choice: ")
    while choice not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input("Enter your choice: ")
    if choice == "1":
        update_config(config, "GAME", "GP_INDEX")
        print("Game version updated to Googleplay successfully.")
    elif choice == "2":
        update_config(config, "GAME", "OS_INDEX")
        print("Game version updated to Overseas successfully.")

def main():
    config = load_config(CONFIG_PATH, DEFAULT_CONFIG)
    
    if not config.get("path"):
        print("Please select a folder to download the files to.")
        folder_path = select_folder()
        if folder_path:
            update_config(config, "path", folder_path)
        else:
            print("No folder selected. Exiting...")
            return
        select_game_version(config)
    
    folder_path = config["path"]
    index = download.url.index(download.url.GAME[config["GAME"]])
    resources = download.url.resources(index)
    cdn = "https://hw-pcdownload-aws.aki-game.net/" + index.default.resourcesBasePath
    
    print("Game selected:", config["GAME"])
    print("1. Install game")
    print("2. Verify game (Resume download if interrupted)")
    print("3. Change download folder")
    print("4. Change Game Version (Googleplay or Overseas)")
    print("5. Exit")
    choice = input("Enter your choice: ")
    
    while True:
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("Selected folder:", folder_path)
            download.start_download(resources, cdn, folder_path, threads=config["threads"])
            print("Game installed successfully.")
            print("Opening game folder...")
            os.startfile(os.path.join(folder_path, "Client/Binaries/Win64/"))
            print("Run Client-Win64-Shipping.exe to start the game")
        elif choice == "2":
            print("Selected folder:", folder_path)
            print("Verifying game...")
            download.verify_game(resources, cdn, folder_path)
            print("Game verified successfully.")
        elif choice == "3":
            folder_path = select_folder()
            if folder_path:
                update_config(config, "path", folder_path)
                print("Download folder updated successfully.")
        elif choice == "4":
            select_game_version(config)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")  # Handle Ctrl+C
        quit(0)
