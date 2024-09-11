import unittest
import os
from unittest.mock import patch, MagicMock
import psycopg2
from dotenv import load_dotenv
from functions import (
    fetch_activities_and_prices_from_database,
    fetch_user_bookings_from_database,
    booking_confirmed,
    delete_booking_from_database,
    fetch_activities_from_database,
    admin_or_not,
    login_credentials_check,
    admin_change_price,
    admin_delete_activity,
    admin_add_activity,
    save_message_to_database,
    fetch_contact_messages_from_database
)

load_dotenv()

# Mocka anslutningsdetaljer
conn_details = {
    "host": os.getenv("DATABASE_HOST"),
    "database": os.getenv("DATABASE_NAME"),
    "user": os.getenv("DATABASE_USER"),
    "password": os.getenv("DATABASE_PASSWORD"),
    "port": os.getenv("DATABASE_PORT")
}
class TestDatabaseFunctions(unittest.TestCase):

    @patch('psycopg2.connect')
    def test_fetch_activities_and_prices_from_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Tennis', 300)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = fetch_activities_and_prices_from_database()
        self.assertEqual(result, [('Tennis', 300)])
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT activity, price FROM court")

    @patch('psycopg2.connect')
    def test_fetch_user_bookings_from_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Tennis', '2024-09-01', '10:00', 'test@example.com', '1234567890', 300)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = fetch_user_bookings_from_database('test@example.com')
        self.assertEqual(result, [('Tennis', '2024-09-01', '10:00', 'test@example.com', '1234567890', 300)])
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM user_bookings_view WHERE email = %s", ('test@example.com',))

    @patch('psycopg2.connect')
    @patch('random.randint')
    def test_booking_confirmed(self, mock_randint, mock_connect):
        mock_cursor = MagicMock()
        mock_randint.return_value = 123456
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = booking_confirmed('Tennis', '2024-09-01', '10:00', 'test@example.com', '1234567890')
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_any_call("SELECT * FROM bookinginformation WHERE booking_id = %s", (123456,))
        mock_cursor.execute.assert_any_call("INSERT INTO bookinginformation (booking_id, activity, date, time, email, phone) VALUES (%s, %s, %s, %s, %s, %s)",
                                            (123456, 'Tennis', '2024-09-01', '10:00', 'test@example.com', '1234567890'))

    @patch('psycopg2.connect')
    def test_delete_booking_from_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = delete_booking_from_database(123456)
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("DELETE FROM bookinginformation WHERE booking_id = %s", (123456,))

    @patch('psycopg2.connect')
    def test_fetch_activities_from_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Tennis',), ('Badminton',)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = fetch_activities_from_database()
        self.assertEqual(result, ['Tennis', 'Badminton'])
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT TRIM(BOTH ',' FROM activity) FROM court")

    @patch('psycopg2.connect')
    def test_admin_or_not(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (True,)
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = admin_or_not('admin@gmail.com')
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT admin FROM inloggningsuppgifter WHERE email = %s", ('admin@gmail.com',))

    @patch('psycopg2.connect')
    def test_login_credentials_check(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('abc123', 'admin@gmail.com', True)]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = login_credentials_check('admin@gmail.com', 'abc123')
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT password, email, admin FROM inloggningsuppgifter WHERE email = %s AND password = %s", ('admin@gmail.com', 'abc123'))

    @patch('psycopg2.connect')
    def test_admin_change_price(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = admin_change_price('Tennis', 350)
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("UPDATE court SET price = %s WHERE activity = %s", (350, 'Tennis'))

    @patch('psycopg2.connect')
    def test_admin_delete_activity(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = admin_delete_activity('Tennis')
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("DELETE FROM court WHERE activity = %s", ('Tennis',))

    @patch('psycopg2.connect')
    def test_admin_add_activity(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = admin_add_activity('Yoga', 50)
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("INSERT INTO court (activity, price) VALUES (%s, %s)", ('Yoga', 50))

    @patch('psycopg2.connect')
    def test_save_message_to_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = save_message_to_database('test@example.com', '1234567890', 'Test message')
        self.assertTrue(result)
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("INSERT INTO contact_messages (email, phone, message) VALUES (%s, %s, %s)", ('test@example.com', '1234567890', 'Test message'))

    @patch('psycopg2.connect')
    def test_fetch_contact_messages_from_database(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('test@example.com', '1234567890', 'Do we have any A-ARON IN THE CLASS?')]
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = fetch_contact_messages_from_database()
        self.assertEqual(result, [('test@example.com', '1234567890', 'Do we have any A-ARON IN THE CLASS?')])
        mock_connect.assert_called_once_with(**conn_details)
        mock_cursor.execute.assert_called_once_with("SELECT email, phone, message FROM contact_messages")

if __name__ == '__main__':
    unittest.main()
