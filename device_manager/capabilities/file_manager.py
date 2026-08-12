import os
import glob
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from config import BASE_DIR, WORKSPACE_DIR, UPLOAD_DIR
from ai.qwen_engine import qwen_engine

class FileManager:
    """
    Windows File System Intelligence Layer.
    Handles scoped file search, folder opening, default app file launching, directory listing, and local AI document summarization.
    """
    def __init__(self):
        user_home = Path(os.path.expanduser("~"))
        self.known_folders: Dict[str, Path] = {
            "downloads": user_home / "Downloads",
            "documents": user_home / "Documents",
            "desktop": user_home / "Desktop",
            "pictures": user_home / "Pictures",
            "videos": user_home / "Videos",
            "music": user_home / "Music",
            "onedrive": user_home / "OneDrive",
            "workspace": WORKSPACE_DIR,
            "project": WORKSPACE_DIR,
            "device manager": WORKSPACE_DIR,
            "uploads": UPLOAD_DIR
        }

    def resolve_folder_path(self, folder_name: str) -> Optional[Path]:
        clean = folder_name.lower().strip().replace("folder", "").strip()
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
            return False, f"Could not find folder '{folder_name}'."

        try:
            os.startfile(str(folder_path))
            return True, f"Opening {folder_path.name} folder."
        except Exception as e:
            return False, f"Failed to open folder '{folder_name}': {str(e)}"

    def search_files(self, query: str, search_dir: Optional[str] = None, ext_filter: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        clean_q = query.lower().strip()
        target_dirs = []

        if search_dir:
            res_dir = self.resolve_folder_path(search_dir)
            if res_dir and res_dir.exists():
                target_dirs.append(res_dir)

        if not target_dirs:
            target_dirs = [
                self.known_folders["downloads"],
                self.known_folders["desktop"],
                self.known_folders["documents"],
                self.known_folders["workspace"]
            ]

        results = []
        for root_dir in target_dirs:
            if not root_dir.exists():
                continue
            try:
                for root, _, files in os.walk(str(root_dir)):
                    # Skip hidden or deep vendor folders
                    if any(ignore in root.lower() for ignore in [".git", "__pycache__", "node_modules", ".venv", "env"]):
                        continue
                    for f in files:
                        f_lower = f.lower()
                        if clean_q in f_lower or clean_q == "*" or not clean_q:
                            if ext_filter and not f_lower.endswith(ext_filter.lower()):
                                continue
                            full_p = Path(root) / f
                            results.append({
                                "name": f,
                                "path": str(full_p),
                                "folder": root,
                                "extension": full_p.suffix
                            })
                            if len(results) >= limit:
                                return results
            except Exception as e:
                print(f"[FILE SEARCH WARNING]: {e}")

        return results

    def open_file(self, file_query: str) -> Tuple[bool, str]:
        # Direct path check
        p = Path(file_query)
        if p.exists() and p.is_file():
            try:
                os.startfile(str(p))
                return True, f"Opening {p.name}."
            except Exception as e:
                return False, f"Failed to open file: {e}"

        # Scoped search
        matches = self.search_files(file_query, limit=3)
        if not matches:
            return False, f"I couldn't find any file matching '{file_query}'."

        if len(matches) == 1:
            target = matches[0]["path"]
            try:
                os.startfile(target)
                return True, f"Opening {matches[0]['name']}."
            except Exception as e:
                return False, f"Failed to open {matches[0]['name']}: {e}"

        # Multiple matches
        names = [m["name"] for m in matches]
        return False, f"I found multiple matching files: {', '.join(names)}. Which one would you like me to open?"

    def create_folder(self, folder_name: str, parent_dir: Optional[str] = None) -> Tuple[bool, str]:
        base = self.resolve_folder_path(parent_dir) if parent_dir else self.known_folders["desktop"]
        if not base:
            base = self.known_folders["desktop"]

        new_dir = base / folder_name
        try:
            new_dir.mkdir(parents=True, exist_ok=True)
            return True, f"Created new folder '{folder_name}' at {base.name}."
        except Exception as e:
            return False, f"Failed to create folder: {str(e)}"

    def read_text_file(self, filepath: str, max_chars: int = 4000) -> Tuple[bool, str]:
        p = Path(filepath)
        if not p.exists() or not p.is_file():
            matches = self.search_files(filepath, limit=1)
            if matches:
                p = Path(matches[0]["path"])
            else:
                return False, f"File '{filepath}' not found."

        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(max_chars)
            return True, content
        except Exception as e:
            return False, f"Could not read file '{p.name}': {e}"

    def summarize_document(self, filepath: str) -> Tuple[bool, str]:
        succ, text = self.read_text_file(filepath)
        if not succ:
            return False, text

        prompt = f"Summarize the following document in 3 clear, concise sentences:\n\n{text[:3000]}"
        reply, tps = qwen_engine.generate_ai_response(prompt)
        if reply:
            return True, reply.strip()
        else:
            return True, f"Document sample from {Path(filepath).name}: {text[:200]}..."

file_manager = FileManager()
