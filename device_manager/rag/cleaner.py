import re

class TextCleaner:
    """
    Cleans and normalizes document text before chunking.
    Preserves Python indentation/comments, Markdown headings, and JSON structures.
    """
    def clean(self, text: str, extension: str) -> str:
        if not text:
            return ""

        # Remove null characters and replace invalid whitespace
        cleaned = text.replace('\x00', '').replace('\r\n', '\n').replace('\r', '\n')

        if extension.lower() == ".py":
            # For Python, collapse excessive empty lines (max 2) but preserve line indentation
            lines = cleaned.split('\n')
            result_lines = []
            empty_count = 0
            for line in lines:
                if not line.strip():
                    empty_count += 1
                    if empty_count <= 2:
                        result_lines.append("")
                else:
                    empty_count = 0
                    result_lines.append(line.rstrip())
            return '\n'.join(result_lines).strip()

        elif extension.lower() in [".md", ".txt"]:
            # Collapse 3+ newlines into double newlines for paragraph breaks
            cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
            # Remove trailing spaces per line
            lines = [l.rstrip() for l in cleaned.split('\n')]
            return '\n'.join(lines).strip()

        elif extension.lower() == ".json":
            # Basic json whitespace normalization
            cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
            return cleaned.strip()

        # Default fallback
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        return cleaned.strip()

cleaner = TextCleaner()
