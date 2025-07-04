import re
from files.list_files import list_files  # Example import
from files.duplicate_files import DuplicateFinder
import os

ALLOWED_ACTIONS = {"list_files", "list_duplicates", "delete_duplicates"}

def parse_prompt(prompt: str):
    prompt = prompt.lower()
    if "list" in prompt and "duplicate" in prompt:
        return "list_duplicates"
    elif "list" in prompt:
        return "list_files"
    elif "delete" in prompt and "duplicate" in prompt:
        return "delete_duplicates"
    # Add more rules as needed
    return "unknown"

def extract_folder(prompt: str):
    # Simple folder extraction (expand as needed)
    match = re.search(r"in ([\w\- ]+)", prompt)
    if match:
        return match.group(1)
    return None

def handle_prompt(prompt: str):
    intent = parse_prompt(prompt)
    folder = extract_folder(prompt) or "Downloads"
    
    # Constraint: Only allow certain actions
    if intent not in ALLOWED_ACTIONS:
        print("Sorry, I can only list files, find duplicates, or delete duplicates right now.")
        return

    # Constraint: Folder must exist
    if not folder_exists(folder):
        print(f"Sorry, the folder '{folder}' does not exist. Please specify a valid folder.")
        return

    # Constraint: Confirm before deleting
    if intent == "delete_duplicates":
        confirm = input(f"Are you sure you want to delete duplicates in {folder}? (yes/no): ").strip().lower()
        if confirm not in ("yes", "y"):
            print("Delete action cancelled.")
            return

    # Proceed with allowed, validated action
    if intent == "list_files":
        print(f"Listing files in {folder}...")
        # list_files(folder)
    elif intent == "list_duplicates":
        print(f"Finding duplicates in {folder}...")
        # finder = DuplicateFinder(folder)
        # print(finder.find_by_name())
    elif intent == "delete_duplicates":
        print(f"Deleting duplicates in {folder}...")
        # finder = DuplicateFinder(folder)
        # ...delete logic...

    # After extracting dest from the prompt:
    roots = get_user_root_dirs()
    if folder:
        for key in roots:
            if folder.lower() == key.lower():
                folder_folder = roots[key]
                if folder:
                    folder = os.path.join(folder_folder, os.path.basename(folder))
                else:
                    folder = str(folder_folder)
                break

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        handle_prompt(user_input) 