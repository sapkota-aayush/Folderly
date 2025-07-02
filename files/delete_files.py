from pathlib import Path
from typing import List, Union
import shutil

class DeleteManager:
    def __init__(self):
        pass

    def delete_single(self, target: Union[str, Path], recursive: bool = False, confirm: bool = True) -> bool:
        """
        Delete a single file or folder. If recursive is True, delete folder and all contents.
        If confirm is True, prompt for confirmation before deleting.
        Returns True if deleted, False otherwise.
        """
        target = Path(target)
        if not target.exists():
            print(f"{target} does not exist.")
            return False
        if confirm:
            resp = input(f"Are you sure you want to delete '{target}'? (y/n): ").lower()
            if resp != 'y':
                print("Delete cancelled.")
                return False
        try:
            if target.is_file() or target.is_symlink():
                target.unlink()
            elif target.is_dir():
                if recursive:
                    shutil.rmtree(target)
                else:
                    target.rmdir()
            print(f"Deleted: {target}")
            return True
        except Exception as e:
            print(f"Error deleting {target}: {e}")
            return False

    def delete_multiple(self, targets: List[Union[str, Path]], recursive: bool = False, confirm: bool = True) -> List[bool]:
        """
        Delete multiple files or folders. Returns a list of booleans indicating success for each delete.
        """
        results = []
        for target in targets:
            result = self.delete_single(target, recursive=recursive, confirm=confirm)
            results.append(result)
        return results 