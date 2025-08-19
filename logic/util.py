import logging
import os
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    # Try to find the project root by looking for the ProjectStorage directory
    current_path = Path(__file__).parent
    while current_path.parent != current_path:  # While not at root
        if (current_path / "ProjectStorage").exists():
            return current_path
        current_path = current_path.parent
    
    # Fallback: go up two levels from logic directory
    return Path(__file__).parent.parent


def setup_storage():
    """Create necessary storage directories if they don't exist."""
    storage_dirs = [
        "ProjectStorage/uploads",
        "ProjectStorage/extracted",
        "ProjectStorage/reports",
        "ProjectStorage/logs",
        "ProjectStorage/screenshots"
    ]
    for dir_path in storage_dirs:
        full_path = Path(get_project_root()) / dir_path
        full_path.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """Configure logging to file and console."""
    log_dir = Path(get_project_root()) / "ProjectStorage" / "logs"
    log_file = log_dir / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
