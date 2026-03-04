import sqlite3
from typing import Dict, Any, Optional
from utils.helpers import setup_logger

logger = setup_logger("Database")

class Database:
    def __init__(self, db_path: str = "linkedin_agent.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the local database and create table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        company TEXT,
                        role TEXT,
                        domain TEXT,
                        email TEXT,
                        phone TEXT,
                        source TEXT,
                        verification_status TEXT,
                        confidence_score INTEGER,
                        email_status TEXT,
                        linkedin_url TEXT,
                        linkedin_message TEXT,
                        linkedin_status TEXT,
                        processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def add_lead(self, lead_data: Dict[str, Any]) -> int:
        """Insert a processed lead into the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                columns = ', '.join(lead_data.keys())
                placeholders = ', '.join(['?' for _ in lead_data])
                values = tuple(lead_data.values())
                
                query = f"INSERT INTO leads ({columns}) VALUES ({placeholders})"
                cursor.execute(query, values)
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to insert lead {lead_data.get('name')}: {e}")
            return -1

    def get_lead_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lead by email to check if already processed."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM leads WHERE email = ?", (email,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            logger.error(f"Failed to retrieve lead by email {email}: {e}")
            return None
