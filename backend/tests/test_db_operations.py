import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from app import db_operations

class TestDBOperations(unittest.TestCase):

    @patch('app.db_operations.psycopg2.connect')
    def test_connect_db_success(self, mock_connect):
        """
        Veritabanı bağlantısının başarılı bir şekilde kurulup kurulmadığını test eder.
        """
        mock_connect.return_value = MagicMock()
        conn = db_operations.connect_db()
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()

    @patch('app.db_operations.psycopg2.connect')
    def test_create_table(self, mock_connect):
        
        """
         Veritabanında bir tablo oluşturma fonksiyonunun doğru çalıştığını test eder.
        """
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Örnek DataFrame
        sample_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        db_operations.create_table('test_table', mock_conn, sample_df)

        # SQL sorgusunun doğru çalışıp çalışmadığını kontrol et
        mock_cursor.execute.assert_called_with(
            'CREATE TABLE test_table (col1 INTEGER, col2 INTEGER);'
        )
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
