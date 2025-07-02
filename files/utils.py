from pathlib import Path

def get_user_root_dirs():
    """
    Returns a dictionary of common user root directories (Desktop, Downloads, Documents, Pictures, Music, Videos)
    that exist on the current system.
    """
    home = Path.home()
    roots = {
        "Desktop": home / "Desktop",
        "Downloads": home / "Downloads",
        "Documents": home / "Documents",
        "Pictures": home / "Pictures",
        "Music": home / "Music",
        "Videos": home / "Videos"
    }
    # Only include folders that actually exist
    return {name: path for name, path in roots.items() if path.exists()} 