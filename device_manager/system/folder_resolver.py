import os
from pathlib import Path
from typing import Optional, Dict

class FolderResolver:
    """
    Dynamic Windows Special Folder Resolver.
    Resolves standard Windows user folders relative to Path.home() / environment variables
    without hardcoding specific username strings.
    """
    def __init__(self):
        self.home = Path.home()
        self.special_folders: Dict[str, Path] = {
            "downloads": self.home / "Downloads",
            "download": self.home / "Downloads",
            "desktop": self.home / "Desktop",
            "documents": self.home / "Documents",
            "document": self.home / "Documents",
            "pictures": self.home / "Pictures",
            "photos": self.home / "Pictures",
            "videos": self.home / "Videos",
            "music": self.home / "Music",
            "appdata": Path(os.environ.get("APPDATA", str(self.home / "AppData" / "Roaming"))),
            "onedrive": self.home / "OneDrive",
            "home": self.home,
            "userprofile": self.home,
        }

    def resolve_folder(self, query: str) -> Optional[Path]:
        if not query:
            return None

        clean = query.lower().strip()
        clean = clean.replace("my ", "").replace("the ", "").replace("folder", "").replace("directory", "").strip()

        # Check known special folder dictionary
        if clean in self.special_folders:
            path = self.special_folders[clean]
            if path.exists():
                return path

        # Check if direct path string under home directory
        possible_path = self.home / clean.capitalize()
        if possible_path.exists():
            return possible_path

        # Check if query is already an absolute path
        try:
            abs_p = Path(query)
            if abs_p.is_absolute() and abs_p.exists():
                return abs_p
        except Exception:
            pass

        return None

    def get_friendly_name(self, path: Path) -> str:
        name = path.name
        if not name:
            return "Home"
        return name.capitalize()

folder_resolver = FolderResolver()
