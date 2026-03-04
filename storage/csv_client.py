import os
import csv
from utils.helpers import setup_logger
from datetime import datetime

logger = setup_logger("CsvClient")

class CsvClient:
    def __init__(self, file_path="leads.csv"):
        self.file_path = file_path
        self._init_csv()

    def _init_csv(self):
        """Initialize the CSV file with headers if it doesn't exist."""
        headers = [
            "Name", "Company", "Role", "Domain", "Email", "Phone", "Source",
            "Verification Status", "Confidence Score", "Email Status", 
            "Email Timestamp", "LinkedIn URL", "LinkedIn Message Draft", 
            "LinkedIn Status", "LinkedIn Timestamp", "Reply Status"
        ]
        
        if not os.path.exists(self.file_path):
            try:
                with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                logger.info(f"Created new CSV file '{self.file_path}' with headers.")
            except Exception as e:
                logger.error(f"Failed to create CSV file: {e}")

    def append_row(self, data: list):
        """Append a new row to the CSV."""
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            logger.info("Successfully appended row to CSV.")
        except Exception as e:
            logger.error(f"Failed to append row to CSV: {e}")

    def update_status(self, row_index: int, col_index: int, value: str):
        """
        Update a specific cell value in the CSV.
        Note: CSV is not ideal for random access updates by row_index/col_index.
        For a more robust solution, the SQLite database should be the primary source of truth,
        and the CSV could be regenerated or updated by searching for a unique ID.
        Here we implement a basic overwrite for the given row/col index (1-based for header).
        """
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as f:
                reader = list(csv.reader(f))
            
            if row_index <= len(reader) and col_index <= len(reader[0]):
                reader[row_index - 1][col_index - 1] = value
                
                with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerows(reader)
                logger.info(f"Updated status at {row_index},{col_index} to {value} in CSV.")
            else:
                logger.warning("Row or column index out of bounds for CSV update.")
        except Exception as e:
            logger.error(f"Failed to update CSV cell: {e}")

    def log_timestamp(self, row_index: int, col_index: int):
        """Log the current timestamp in a specific cell."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_status(row_index, col_index, timestamp)
