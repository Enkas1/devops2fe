from functions import fetch_activities_and_prices_from_database, delete_booking_from_database
from unittest.mock import patch
from unittest.mock import MagicMock




@patch('functions.psycopg2.connect')
def test_fetch_activities_and_prices_from_database(mock_connect):
    mock_activity_prices = [('Tennis', 100), ('Padel', 150)]
    # Mocka cursor och fetchall-metoder
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = mock_activity_prices

    # Kör funktionen
    result = fetch_activities_and_prices_from_database()

    # Kontrollera att psycopg2.connect anropades en gång
    mock_connect.assert_called_once()

    # Kontrollera att den korrekta SQL-frågan exekverades
    mock_cursor.execute.assert_called_once_with("SELECT activity, price FROM court")

    # Kontrollera att resultatet är som förväntat
    assert result == mock_activity_prices

@patch('functions.psycopg2.connect')
def test_delete_booking_from_database(mock_connect):
    # Testdata
    booking_id_to_delete = 12345

    # Mocka cursor och commit-metoder
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # Simulera att 1 rad tas bort
    mock_cursor.rowcount = 1

    # Kör funktionen
    result = delete_booking_from_database(booking_id_to_delete)

    # Kontrollera att psycopg2.connect anropades en gång
    mock_connect.assert_called_once()

    # Kontrollera att cursor.execute anropades med rätt SQL-fråga och parametrar
    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM bookinginformation WHERE booking_id = %s",
        (booking_id_to_delete,)
    )

    # Kontrollera att commit anropades en gång
    mock_connection.commit.assert_called_once()

    # Kontrollera att resultatet är True
    assert result is True
