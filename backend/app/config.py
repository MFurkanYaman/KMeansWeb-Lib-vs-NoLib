from pathlib import Path

# Kök dizini
BASE_DIR = Path(__file__).resolve().parent

# Veritabanı bilgileri
DB_HOST = "localhost"
DB_NAME = "dbKmeans"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_PORT = "5432"

# Log bilgileri
LOG_FILE="backend/log file/app_errors.log"

# Sonuç bilgileri
RESULT_FILE = (BASE_DIR / 'static' / 'results' / 'result.csv').as_posix()

# Veri bilgileri
UPLOADER_FOLDER = "backend/data"

# Görsel klasörü
IMG_FOLDER = (BASE_DIR / 'static' / 'images').as_posix() + "/"
