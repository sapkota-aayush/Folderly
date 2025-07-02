from pathlib import Path
from typing import List, Union
import shutil
import os

class CopyManager:
    def __init__(self):
        pass

    def copy_single(self, src: Union[str, Path], dest: Union[str, Path], overwrite: bool = False) -> bool:
        """
        Copy a single file or folder to the destination.
        If overwrite is False and destination exists, skip and return False.
        Returns True if copied, False otherwise.
        """
        src = Path(src)
        dest = Path(dest)
        if dest.exists():
            if overwrite:
                if dest.is_file() or dest.is_symlink():
                    dest.unlink()
                elif dest.is_dir():
                    shutil.rmtree(dest)
            else:
                return False
        try:
            if src.is_file():
                shutil.copy2(str(src), str(dest))
            elif src.is_dir():
                shutil.copytree(str(src), str(dest))
            else:
                print(f"{src} is not a file or directory.")
                return False
            return True
        except Exception as e:
            print(f"Error copying {src} to {dest}: {e}")
            return False

    def copy_multiple(self, sources: List[Union[str, Path]], dest_folder: Union[str, Path], overwrite: bool = False) -> List[bool]:
        """
        Copy multiple files or folders to the destination folder.
        Returns a list of booleans indicating success for each copy.
        """
        dest_folder = Path(dest_folder)
        results = []
        for src in sources:
            src = Path(src)
            dest = dest_folder / src.name
            result = self.copy_single(src, dest, overwrite=overwrite)
            results.append(result)
        return results 