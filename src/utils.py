"""
Utility Functions Module
Provides common helper functions for PDF mail merge operations.
"""

import os
import shutil
import zipfile
import hashlib
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime


def ensure_dir(directory: str) -> bool:
    """
    Ensure directory exists, create if not.

    Args:
        directory: Path to directory

    Returns:
        True if directory exists or was created
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False


def clean_dir(directory: str) -> bool:
    """
    Clean directory by removing all files and subdirectories.

    Args:
        directory: Path to directory

    Returns:
        True if successful
    """
    try:
        target = Path(directory).resolve()
        protected = (Path.cwd().resolve(), Path.home().resolve())
        if target == Path(target.anchor) or target in protected or any(target in p.parents for p in protected):
            raise ValueError("Refusing to clean a root, home, or working directory")
        if Path(directory).is_symlink():
            raise ValueError("Refusing to clean a symbolic link")
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error cleaning directory {directory}: {e}")
        return False


def get_file_hash(file_path: str, algorithm: str = "md5") -> str:
    """
    Calculate file hash.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256')

    Returns:
        Hex digest of file hash
    """
    try:
        if algorithm == "md5":
            hasher = hashlib.md5()
        elif algorithm == "sha1":
            hasher = hashlib.sha1()
        else:
            hasher = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)

        return hasher.hexdigest()
    except Exception:
        return ""


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List all files in directory with optional extension filter.

    Args:
        directory: Path to directory
        extension: File extension filter (e.g., '.pdf')

    Returns:
        List of file paths
    """
    try:
        files = []
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if extension is None or filename.endswith(extension):
                    files.append(os.path.join(root, filename))
        return files
    except Exception:
        return []


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human-readable string.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., '1.5 MB')
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_timestamp() -> str:
    """
    Get current timestamp string.

    Returns:
        Timestamp in format 'YYYYMMDD_HHMMSS'
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def create_zip_archive(
    source_dir: str, output_path: str, include_subdirs: bool = True
) -> bool:
    """
    Create ZIP archive from directory.

    Args:
        source_dir: Source directory path
        output_path: Output ZIP file path
        include_subdirs: Include subdirectory structure

    Returns:
        True if successful
    """
    try:
        if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
            print(f"Source directory does not exist: {source_dir}")
            return False

        ensure_dir(os.path.dirname(output_path) or ".")

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            if include_subdirs:
                for root, dirs, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        if Path(file_path).resolve() != Path(output_path).resolve():
                            zipf.write(file_path, arcname)
            else:
                for file in os.listdir(source_dir):
                    file_path = os.path.join(source_dir, file)
                    if os.path.isfile(file_path):
                        if Path(file_path).resolve() != Path(output_path).resolve():
                            zipf.write(file_path, os.path.basename(file_path))

        return True

    except Exception as e:
        print(f"Error creating ZIP archive: {e}")
        return False


def extract_zip_archive(zip_path: str, output_dir: str) -> bool:
    """
    Extract ZIP archive to directory.

    Args:
        zip_path: Path to ZIP file
        output_dir: Output directory

    Returns:
        True if successful
    """
    try:
        ensure_dir(output_dir)

        with zipfile.ZipFile(zip_path, "r") as zipf:
            root = Path(output_dir).resolve()
            for name in zipf.namelist():
                normalized = name.replace("\\", "/")
                destination = (root / normalized).resolve()
                if destination != root and root not in destination.parents:
                    raise ValueError("ZIP entry escapes the destination directory")
            zipf.extractall(output_dir)

        return True

    except Exception as e:
        print(f"Error extracting ZIP archive: {e}")
        return False


def parse_naming_pattern(
    pattern: str, data: Dict[str, any], default: str = "document"
) -> str:
    """
    Parse naming pattern with data fields.

    Args:
        pattern: Naming pattern with {field} placeholders
        data: Data dictionary for replacement
        default: Default name if pattern produces empty result

    Returns:
        Parsed filename
    """
    try:
        filename = pattern

        for key, value in data.items():
            placeholder = f"{{{key}}}"
            if placeholder in filename:
                safe_value = str(value).replace("/", "_").replace("\\", "_")
                safe_value = safe_value.replace(":", "_").replace("*", "_")
                safe_value = safe_value.replace("?", "_").replace('"', "_")
                safe_value = safe_value.replace("<", "_").replace(">", "_")
                safe_value = safe_value.replace("|", "_")
                filename = filename.replace(placeholder, safe_value)

        filename = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", filename).strip().rstrip(". ")
        if not filename or filename in (".", ".."):
            filename = default
        if re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)", filename, re.I):
            filename = "_" + filename
        return filename[:150].rstrip(". ")

    except Exception:
        return default


def validate_path(path: str, must_exist: bool = True) -> Tuple[bool, str]:
    """
    Validate file or directory path.

    Args:
        path: Path to validate
        must_exist: Whether path must already exist

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path:
        return False, "Path is empty"

    if must_exist and not os.path.exists(path):
        return False, f"Path does not exist: {path}"

    if must_exist and os.path.isdir(path):
        try:
            with tempfile.TemporaryFile(dir=path):
                pass
        except Exception:
            return False, f"Directory is not writable: {path}"

    return True, ""


def get_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Generate text-based progress bar.

    Args:
        current: Current progress value
        total: Total value
        width: Width of progress bar in characters

    Returns:
        Progress bar string
    """
    if total == 0:
        percent = 100
    else:
        percent = int(100 * current / total)

    filled = int(width * current / total) if total > 0 else 0
    bar = "=" * filled + "-" * (width - filled)

    return f"[{bar}] {percent}% ({current}/{total})"


def print_progress(
    current: int, total: int, prefix: str = "", suffix: str = "", width: int = 50
) -> None:
    """
    Print progress bar to console.

    Args:
        current: Current progress value
        total: Total value
        prefix: Prefix text
        suffix: Suffix text
        width: Width of progress bar
    """
    bar = get_progress_bar(current, total, width)
    line = f"\r{prefix} {bar} {suffix}"
    print(line, end="", flush=True)

    if current >= total:
        print()


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        s: String to truncate
        max_length: Maximum length
        suffix: Suffix to append if truncated

    Returns:
        Truncated string
    """
    if len(s) <= max_length:
        return s

    return s[: max_length - len(suffix)] + suffix


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"


def is_pdf_file(file_path: str) -> bool:
    """
    Check if file is a valid PDF.

    Args:
        file_path: Path to file

    Returns:
        True if file is PDF
    """
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, "rb") as f:
            header = f.read(5)
            return header.startswith(b"%PDF")
    except Exception:
        return False


def get_pdf_stats(output_dir: str) -> Dict[str, any]:
    """
    Get statistics for generated PDF files.

    Args:
        output_dir: Directory containing PDFs

    Returns:
        Dictionary with statistics
    """
    stats = {
        "total_files": 0,
        "total_size": 0,
        "avg_size": 0,
        "smallest": None,
        "largest": None,
    }

    files = list_files(output_dir, ".pdf")

    if files:
        stats["total_files"] = len(files)
        sizes = []

        for file in files:
            size = os.path.getsize(file)
            stats["total_size"] += size
            sizes.append((file, size))

        if sizes:
            stats["avg_size"] = stats["total_size"] / len(sizes)
            sizes.sort(key=lambda x: x[1])
            stats["smallest"] = sizes[0]
            stats["largest"] = sizes[-1]

    return stats
