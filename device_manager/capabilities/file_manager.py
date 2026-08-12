import os
import glob
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from config import BASE_DIR, WORKSPACE_DIR, UPLOAD_DIR
from system.folder_resolver import folder_resolver
from system.window_context import window_context
from ai.qwen_engine import qwen_engine

class FileManager:
    """
    Windows File System Intelligence Layer.
    Handles scoped file search, folder opening, default app file launching, directory listing, and local AI document summarization.
    """
    def __init__(self):
        user_home = Path.home()
        self.known_folders: Dict[str, Path] = {
            "downloads": user_home / "Downloads",
            "documents": user_home / "Documents",
            "desktop": user_home / "Desktop",
            "pictures": user_home / "Pictures",
            "videos": user_home / "Videos",
            "music": user_home / "Music",
            "onedrive": user_home / "OneDrive",
            "appdata": Path(os.environ.get("APPDATA", str(user_home / "AppData" / "Roaming"))),
            "workspace": WORKSPACE_DIR,
            "project": WORKSPACE_DIR,
            "device manager": WORKSPACE_DIR,
            "uploads": UPLOAD_DIR
        }

    def resolve_folder_path(self, folder_name: str) -> Optional[Path]:
        resolved = folder_resolver.resolve_folder(folder_name)
        if resolved:
            return resolved

        clean = folder_name.lower().strip().replace("folder", "").replace("directory", "").strip()
        if clean in self.known_folders:
            return self.known_folders[clean]

        for k, path in self.known_folders.items():
            if clean in k or k in clean:
                return path

        direct_path = Path(folder_name)
        if direct_path.is_dir():
            return direct_path

        return None

    def open_folder(self, folder_name: str) -> Tuple[bool, str]:
        folder_path = self.resolve_folder_path(folder_name)
        if not folder_path or not folder_path.exists():
            return False, f"I couldn't find that folder, boss."

        friendly_name = folder_resolver.get_friendly_name(folder_path)

        # Check if already active window
        active_info = window_context.get_active_window_info()
        active_title = active_info.get("title", "").lower()
        if friendly_name.lower() in active_title and "explorer" in active_info.get("app_alias", "").lower():
            return True, f"{friendly_name} is already open, boss."

        try:
            os.startfile(str(folder_path))
            return True, f"Opening {friendly_name}, boss."
        except Exception as e:
            return False, f"Failed to open folder '{friendly_name}': {str(e)}"

    def search_files(self, query: str, search_dir: Optional[str] = None, ext_filter: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        clean_q = query.lower().strip()
        target_dirs = []

        if search_dir:
            res_dir = self.resolve_folder_path(search_dir)
            if res_dir and res_dir.exists():
                target_dirs.append(res_dir)

        if not target_dirs:
            target_dirs = [self.known_folders["downloads"], self.known_folders["documents"], self.known_folders["desktop"], WORKSPACE_DIR]

        results = []
        for tdir in target_dirs:
            if not tdir.exists():
                continue
            try:
                for root, _, files in os.walk(str(tdir)):
                    for fname in files:
                        if clean_q in fname.lower():
                            if ext_filter and not fname.lower().endswith(ext_filter.lower()):
                                continue
                            fpath = Path(root) / fname
                            results.append({
                                "name": fname,
                                "path": str(fpath),
                                "folder": Path(root).name,
                                "size_bytes": fpath.stat().st_size if fpath.exists() else 0
                            })
                            if len(results) >= limit:
                                return results
            except Exception:
                pass
        return results

    def read_file_content(self, file_path: str, max_chars: int = 3000) -> Tuple[bool, str]:
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            return False, f"File '{file_path}' does not exist."
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(max_chars)
            return True, content
        except Exception as e:
            return False, f"Error reading file '{file_path}': {str(e)}"

    def summarize_file(self, file_path: str) -> Tuple[bool, str]:
        succ, text = self.read_file_content(file_path)
        if not succ:
            return False, text
        prompt = (
            "Summarize the following file content in 3 clear bullet points:\n"
            f"File: {Path(file_path).name}\nContent:\n{text[:2000]}\nSummary:"
        )
        summary, _ = qwen_engine.generate_ai_response(prompt)
        return True, summary

file_manager = FileManager()
