from files.utils import get_user_root_dirs
from files.validate import validate_directory
from files.list_files import FileLister
from files.recursive_list import RecursiveLister
from files.move_files import MoveManager
from pathlib import Path

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
    mover = MoveManager()

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
        print("8. Move a single file/folder")
        print("9. Move multiple files/folders (comma separated)")
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
        elif op == "8":
            src = input("Enter the full path of the file/folder to move: ")
            dest_dir = input("Enter the destination directory: ")
            try:
                validate_directory(dest_dir)
                src_path = Path(src)
                dest_path = Path(dest_dir) / src_path.name
                result = mover.move_single(src_path, dest_path)
                if result:
                    print(f"Moved {src_path} to {dest_path}")
                else:
                    print(f"Failed to move {src_path} to {dest_path}")
            except Exception as e:
                print(f"Error: {e}")
        elif op == "9":
            srcs = input("Enter full paths of files/folders to move (comma separated): ").split(",")
            dest_dir = input("Enter the destination directory: ")
            try:
                validate_directory(dest_dir)
                src_paths = [Path(s.strip()) for s in srcs]
                dest_path = Path(dest_dir)
                results = mover.move_multiple(src_paths, dest_path)
                for src_path, result in zip(src_paths, results):
                    if result:
                        print(f"Moved {src_path} to {dest_path / src_path.name}")
                    else:
                        print(f"Failed to move {src_path} to {dest_path / src_path.name}")
            except Exception as e:
                print(f"Error: {e}")
        elif op == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()