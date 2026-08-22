"""Automated Submission Packaging Utility for HCL Tech Hackathon (Round 2).

Generates a clean source code ZIP archive excluding virtual environments,
git tracking files, caches, and unnecessary build artifacts.
"""

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_ZIP = PROJECT_ROOT / "submission.zip"

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".idea",
    ".vscode",
    ".gemini",
    "dist",
    "build"
}

EXCLUDE_FILES = {
    ".DS_Store",
    "submission.zip",
    ".skillpath_state.json",
    ".env"
}

def create_submission_zip() -> Path:
    """Packages the repository into a clean submission.zip archive."""
    print(f"📦 Packaging clean submission archive from {PROJECT_ROOT}...")
    
    if OUTPUT_ZIP.exists():
        OUTPUT_ZIP.unlink()

    included_count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]

            for file in files:
                if file in EXCLUDE_FILES or file.endswith((".pyc", ".pyo", ".zip")):
                    continue
                
                full_path = Path(root) / file
                rel_path = full_path.relative_to(PROJECT_ROOT)
                
                zipf.write(full_path, rel_path)
                included_count += 1

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"✅ Successfully created {OUTPUT_ZIP.name} ({included_count} files, {size_mb:.2f} MB)")
    return OUTPUT_ZIP

if __name__ == "__main__":
    create_submission_zip()
