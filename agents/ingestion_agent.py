import os
import shutil
from typing import List
from utils.helpers import setup_logger

logger = setup_logger("IngestionAgent")

class IngestionAgent:
    def __init__(self, input_dir: str = "data/input_pdfs", processed_dir: str = "data/processed"):
        self.input_dir = input_dir
        self.processed_dir = processed_dir
        self._ensure_dirs()

    def _ensure_dirs(self):
        """Ensure the input and processed directories exist."""
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)

    def scan_folder(self) -> List[str]:
        """Scan input folder for unprocessed PDFs."""
        pdfs = []
        for file in os.listdir(self.input_dir):
            if file.lower().endswith('.pdf'):
                pdfs.append(os.path.join(self.input_dir, file))
        
        logger.info(f"Found {len(pdfs)} unprocessed PDFs.")
        return pdfs

    def mark_processed(self, filepath: str):
        """Move processed file to the processed directory."""
        try:
            filename = os.path.basename(filepath)
            dest = os.path.join(self.processed_dir, filename)
            shutil.move(filepath, dest)
            logger.info(f"Moved {filename} to {self.processed_dir}")
        except Exception as e:
            logger.error(f"Failed to move processed file {filepath}: {e}")
