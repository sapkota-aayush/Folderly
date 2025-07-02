from pathlib import Path
from typing import Dict, List, Union, Optional
import hashlib

class DuplicateFinder:
    def __init__(self, directory: Union[str, Path], recursive: bool = False, extension: Optional[str] = None):
        self.directory = Path(directory)
        self.recursive = recursive
        self.extension = extension

    def _get_files(self) -> List[Path]:
        if self.recursive:
            files = [f for f in self.directory.rglob('*') if f.is_file()]
        else:
            files = [f for f in self.directory.iterdir() if f.is_file()]
        if self.extension:
            files = [f for f in files if f.suffix == self.extension]
        return files

    def find_by_name(self) -> Dict[str, List[Path]]:
        """Find duplicate files by name."""
        files = self._get_files()
        name_map = {}
        for f in files:
            name_map.setdefault(f.name, []).append(f)
        return {k: v for k, v in name_map.items() if len(v) > 1}

    def find_by_size(self) -> Dict[int, List[Path]]:
        """Find duplicate files by size."""
        files = self._get_files()
        size_map = {}
        for f in files:
            size_map.setdefault(f.stat().st_size, []).append(f)
        return {k: v for k, v in size_map.items() if len(v) > 1}

    def find_by_hash(self, hash_algo: str = 'sha256', chunk_size: int = 8192) -> Dict[str, List[Path]]:
        """Find duplicate files by content hash (default: sha256)."""
        files = self._get_files()
        hash_map = {}
        for f in files:
            h = hashlib.new(hash_algo)
            try:
                with f.open('rb') as file:
                    while chunk := file.read(chunk_size):
                        h.update(chunk)
                file_hash = h.hexdigest()
                hash_map.setdefault(file_hash, []).append(f)
            except Exception as e:
                print(f"Error hashing {f}: {e}")
        return {k: v for k, v in hash_map.items() if len(v) > 1} 