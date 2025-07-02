from files.utils import get_user_root_dirs
from files.validate import validate_directory
from files.list_files import FileLister
from files.recursive_list import RecursiveLister

def main():
    roots = get_user_root_dirs()
    print("Available root folders:")
    for idx, (name, path) in enumerate(roots.items(), 1):
        print(f"{idx}. {name}: {path}")

    # Let user pick a folder
    choice = input("Select a folder by number: ")
    try:
        choice = int(choice)
        folder_name = list(roots.keys())[choice - 1]
        folder_path = roots[folder_name]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Validate the folder
    try:
        validate_directory(str(folder_path))
    except Exception as e:
        print(f"Validation error: {e}")
        return

    lister = FileLister(str(folder_path))
    rec_lister = RecursiveLister(str(folder_path))

    # Menu for file operations
    while True:
        print("\nWhat would you like to do?")
        print("1. List all items")
        print("2. List only files")
        print("3. List only folders")
        print("4. List files by extension")
        print("5. List all files recursively")
        print("6. List files recursively by extension")
        print("7. List all folders recursively")
        print("0. Exit")
        op = input("Enter your choice: ")

        if op == "1":
            print(lister.list_all())
        elif op == "2":
            print(lister.list_files())
        elif op == "3":
            print(lister.list_folders())
        elif op == "4":
            ext = input("Enter file extension (e.g., .txt): ")
            print(lister.list_by_extension(ext))
        elif op == "5":
            print(rec_lister.list_files_recursive())
        elif op == "6":
            ext = input("Enter file extension (e.g., .txt): ")
            print(rec_lister.list_files_recursive(ext))
        elif op == "7":
            print(rec_lister.list_folders_recursive())
        elif op == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()