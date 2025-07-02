from pathlib import Path
from typing import List, Union
import shutil

class MoveManager:
    def __init__(self):
        pass

    def move_single(self, src: Union[str, Path], dest: Union[str, Path], overwrite: bool = False) -> bool:
        """
        Move a single file or folder to the destination.
        If overwrite is False and destination exists, skip and return False.
        Returns True if moved, False otherwise.
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
            shutil.move(str(src), str(dest))
            return True
        except Exception as e:
            print(f"Error moving {src} to {dest}: {e}")
            return False

    def move_multiple(self, sources: List[Union[str, Path]], dest_folder: Union[str, Path], overwrite: bool = False) -> List[bool]:
        """
        Move multiple files or folders to the destination folder.
        Returns a list of booleans indicating success for each move.
        """
        dest_folder = Path(dest_folder)
        results = []
        for src in sources:
            src = Path(src)
            dest = dest_folder / src.name
            result = self.move_single(src, dest, overwrite=overwrite)
            results.append(result)
        return results 