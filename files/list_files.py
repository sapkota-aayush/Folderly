from pathlib import Path
from typing import List, Optional
from datetime import datetime

class FileLister:
    def __init__(self, directory: str):
        self.directory = Path(directory)

    def list_all(self) -> List[Path]:
        """List all files and folders in the directory."""
        return list(self.directory.iterdir())

    def list_files(self) -> List[Path]:
        """List only files."""
        return [f for f in self.directory.iterdir() if f.is_file()]

    def list_folders(self) -> List[Path]:
        """List only folders."""
        return [f for f in self.directory.iterdir() if f.is_dir()]

    def list_by_extension(self, extension: str) -> List[Path]:
        """List files by extension (e.g., '.txt')."""
        return [f for f in self.list_files() if f.suffix == extension]

    def list_by_date(self, after: Optional[datetime] = None, before: Optional[datetime] = None) -> List[Path]:
        """List files modified after/before certain dates."""
        result = []
        for f in self.list_files():
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if (after is None or mtime > after) and (before is None or mtime < before):
                result.append(f)
        return result 