from pathlib import Path
from typing import List, Optional

class RecursiveLister:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def list_files_recursive(self, extension: Optional[str] = None) -> List[Path]:
        """List all files in the directory and its subdirectories, optionally filtered by extension."""
        files = [f for f in self.directory.rglob('*') if f.is_file()]
        if extension:
            files = [f for f in files if f.suffix == extension]
        return files

    def list_folders_recursive(self) -> List[Path]:
        """List all folders in the directory and its subdirectories."""
        return [f for f in self.directory.rglob('*') if f.is_dir()] 