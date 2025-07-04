import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import re
from files.list_files import FileLister
from files.duplicate_files import DuplicateFinder
from files.utils import get_user_root_dirs
from files.copy_files import CopyManager
from files.delete_files import DeleteManager
from files.move_files import MoveManager
from files.recursive_list import RecursiveLister
from files.validate import validate_directory
import os

ALLOWED_ACTIONS = {
    "list_files", "list_folders", "list_duplicates", "delete_duplicates",
    "move_file", "copy_file", "delete_file", "list_files_recursive", "list_folders_recursive"
}

# --- Intent Parsing ---
def parse_prompt(prompt: str):
    prompt = prompt.lower()
    if "list" in prompt and "duplicate" in prompt:
        return "list_duplicates"
    elif "delete" in prompt and "duplicate" in prompt:
        return "delete_duplicates"
    elif "move" in prompt:
        return "move_file"
    elif "copy" in prompt:
        return "copy_file"
    elif "delete" in prompt:
        return "delete_file"
    elif "list" in prompt and "folder" in prompt:
        if "recursive" in prompt or "all" in prompt:
            return "list_folders_recursive"
        return "list_folders"
    elif "list" in prompt and ("recursive" in prompt or "all" in prompt):
        return "list_files_recursive"
    elif "list" in prompt:
        return "list_files"
    return "unknown"

def extract_path(prompt: str, keyword: str = None):
    # Extract quoted path or after keyword
    if '"' in prompt:
        matches = re.findall(r'"([^"]+)"', prompt)
        if matches:
            return matches[0]
    if keyword:
        match = re.search(rf'{keyword} ([^ ]+)', prompt)
        if match:
            return match.group(1)
    return None

def extract_folder(prompt: str):
    roots = get_user_root_dirs()
    for name in roots:
        if name.lower() in prompt:
            return str(roots[name])
    match = re.search(r"in ([\w\- ]+)", prompt)
    if match:
        return os.path.expanduser(match.group(1))
    return None

def folder_exists(folder: str):
    return os.path.isdir(folder)

def extract_dest(prompt: str):
    # Try to extract quoted destination after 'to'
    matches = re.findall(r'to\s+"([^"]+)"', prompt, re.IGNORECASE)
    if matches:
        return matches[0]
    # Try to extract after 'to ' (not quoted)
    match = re.search(r'to\s+([\w\- ]+)', prompt, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

# --- Middle Layer ---
def handle_prompt(prompt: str):
    intent = parse_prompt(prompt)
    folder = extract_folder(prompt)
    src = extract_path(prompt, "from") or extract_path(prompt, "move") or extract_path(prompt, "copy")
    dest = extract_dest(prompt)

    # Resolve destination if it's a known folder name (case-insensitive)
    roots = get_user_root_dirs()
    if dest:
        for key in roots:
            if dest.lower() == key.lower():
                dest_folder = roots[key]
                if src:
                    dest = os.path.join(dest_folder, os.path.basename(src))
                else:
                    dest = str(dest_folder)
                break

    # Prevent moving/copying to the same path
    if src and dest and os.path.abspath(src) == os.path.abspath(dest):
        print("Source and destination are the same. Please specify a different destination.")
        return

    if intent not in ALLOWED_ACTIONS:
        print("Sorry, I can list files/folders, find/delete duplicates, move, copy, or delete files/folders.")
        return

    if intent in ("list_files", "list_folders", "list_duplicates", "delete_duplicates") and not folder:
        print("Please specify a folder (e.g., Desktop, Downloads, Documents, etc.).")
        return
    if folder and not folder_exists(folder):
        print(f"Sorry, the folder '{folder}' does not exist. Please specify a valid folder.")
        return

    try:
        if intent == "list_files":
            print(f"Listing files in {folder}:")
            lister = FileLister(folder)
            files = lister.list_files()
            for f in files:
                print(f)
            if not files:
                print("(No files found)")
        elif intent == "list_folders":
            print(f"Listing folders in {folder}:")
            lister = FileLister(folder)
            folders = lister.list_folders()
            for f in folders:
                print(f)
            if not folders:
                print("(No folders found)")
        elif intent == "list_files_recursive":
            print(f"Recursively listing all files in {folder}:")
            lister = RecursiveLister(folder)
            files = lister.list_files_recursive()
            for f in files:
                print(f)
            if not files:
                print("(No files found)")
        elif intent == "list_folders_recursive":
            print(f"Recursively listing all folders in {folder}:")
            lister = RecursiveLister(folder)
            folders = lister.list_folders_recursive()
            for f in folders:
                print(f)
            if not folders:
                print("(No folders found)")
        elif intent == "list_duplicates":
            print(f"Finding duplicates in {folder}:")
            finder = DuplicateFinder(folder)
            dups = finder.find_by_hash()
            if not dups:
                print("No duplicate files found.")
            else:
                for hashval, paths in dups.items():
                    print(f"Duplicate group (hash: {hashval}):")
                    for p in paths:
                        print(f"  - {p}")
        elif intent == "delete_duplicates":
            print(f"Deleting duplicates in {folder}:")
            finder = DuplicateFinder(folder)
            dups = finder.find_by_hash()
            deleted = 0
            for paths in dups.values():
                for p in paths[1:]:
                    os.remove(p)
                    print(f"Deleted: {p}")
                    deleted += 1
            if deleted == 0:
                print("No duplicate files to delete.")
            else:
                print(f"Deleted {deleted} duplicate files.")
        elif intent == "move_file":
            if not src or not dest:
                print("Please specify both the source file and the destination folder (e.g., move \"file\" to Desktop).")
                return
            print(f"Moving {src} to {dest}...")
            mover = MoveManager()
            success = mover.move_single(src, dest, overwrite=True)
            if success:
                print(f"Moved {src} to {dest}.")
            else:
                print(f"Failed to move {src} to {dest}.")
        elif intent == "copy_file":
            if not src or not dest:
                print("Please specify both the source file and the destination folder (e.g., copy \"file\" to Desktop).")
                return
            print(f"Copying {src} to {dest}...")
            copier = CopyManager()
            success = copier.copy_single(src, dest, overwrite=True)
            if success:
                print(f"Copied {src} to {dest}.")
            else:
                print(f"Failed to copy {src} to {dest}.")
        elif intent == "delete_file":
            if not src:
                print("Please specify the file or folder to delete (e.g., delete \"file\").")
                return
            print(f"Deleting {src}...")
            deleter = DeleteManager()
            success = deleter.delete_single(src, confirm=True)
            if success:
                print(f"Deleted {src}.")
            else:
                print(f"Failed to delete {src}.")
    except Exception as e:
        print(f"An error occurred while processing your request: {e}")

if __name__ == "__main__":
    print("Welcome to Folderly CLI! Type 'exit' or 'quit' to leave.")
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            try:
                handle_prompt(user_input)
            except Exception as e:
                print(f"An error occurred while processing your request: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break 