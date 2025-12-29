import re

def safe_filename(name: str) -> str:
    """
    Converts company names into Windows-safe filenames
    """
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', '', name)  # remove invalid chars
    name = re.sub(r"\s+", "_", name)          # spaces → underscores
    return name[:120]                          # prevent long filenames
