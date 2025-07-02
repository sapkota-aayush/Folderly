from pathlib import Path

def validate_directory(path_str: str) -> Path:
    """Validate that the path exists and is a directory. Return Path object if valid, else raise error."""
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Directory '{path_str}' does not exist.")
    if not path.is_dir():
        raise NotADirectoryError(f"'{path_str}' is not a directory.")
    return path 