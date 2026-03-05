import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure the project root is in path
sys.path.append(os.getcwd())

from send_emails import process_email_queue

class TestEmailOutreach(unittest.TestCase):
    @patch('send_emails.EmailService')
    @patch('send_emails.Database')
    @patch('send_emails.CsvClient')
    @patch('ai.message_generator.MessageGenerator.create_outreach_email')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="Name,Company,Role,Domain,Email,Phone,Source,Verification Status,Confidence Score,Email Status,Email Timestamp,LinkedIn URL,LinkedIn Message Draft,LinkedIn Status,LinkedIn Timestamp,Reply Status\nJohn Doe,TechCorp,CEO,techcorp.com,john@techcorp.com,,PDF Processing,verified,100,queued,,,,,,")
    def test_process_email_queue(self, mock_open, mock_exists, mock_create_email, mock_csv, mock_db, mock_email_service):
        mock_exists.return_value = True
        mock_email_instance = mock_email_service.return_value
        mock_email_instance.send_email.return_value = True
        
        mock_create_email.return_value = {"subject": "Test Subject", "body": "Test Body"}
        
        process_email_queue()
        
        # Verify email was "sent"
        mock_email_instance.send_email.assert_called_once_with("john@techcorp.com", "Test Subject", "Test Body")
        
        # Verify CSV was updated (mock_open called for write)
        # The script calls open twice: once for read, once for write.
        self.assertEqual(mock_open.call_count, 2)
        
if __name__ == '__main__':
    unittest.main()
