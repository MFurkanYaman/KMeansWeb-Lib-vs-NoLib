import logging

import psycopg2
import pandas as pd

from app import config

def connect_db():
    """
    Bu fonksiyon, PostgreSQL veritabanına bağlanır ve bağlantı nesnesini döner.

    Return:
        connection: Veritabanı bağlantı nesnesi.

    Yaptığı İşlemler:
        1. Veritabanı bağlantı bilgilerini config'den alır.
        2. Veritabanına bağlanmayı dener ve başarılı olursa bağlantıyı döner.
        3. Bağlantı sırasında hata oluşursa loglara hata yazar.

    """
    try:
        # connection = psycopg2.connect(
        #     host=config.DB_HOST,
        #     port=config.DB_PORT,
        #     database=config.DB_NAME,
        #     user=config.DB_USER,
        #     password=config.DB_PASSWORD
        # )
        connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "dbKmeans"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "1234"),
        port=os.getenv("DB_PORT", "5432")
    )
        logging.info("Successfully connected to database.")
        return connection

    except Exception as e:
       logging.error(f"connection_db named function -{e}")
    
def create_table(table_name,conn,csv_df,sayac=0):
    """
    Bu fonksiyon, verilen veriye dayanarak PostgreSQL veritabanında bir tablo oluşturur.

    Parametreler:
        table_name: Oluşturulacak tablonun adı (string).
        conn: Veritabanı bağlantı nesnesi.
        csv_df: Tablo yapısı için kullanılan pandas DataFrame (veri çerçevesi).
        sayac: Aynı isimde bir tablo varsa tabloyu silme kararını belirler (0 veya 1).

    Yaptığı İşlemler:
        1. Veritabanında aynı isimde bir tablo olup olmadığını kontrol eder.
        2. Eğer tablo varsa ve sayac 0 ise, tabloyu siler.
        3. DataFrame'deki sütun adlarına göre tabloyu yeniden oluşturur.
        4. Tabloyu veritabanına kaydeder.
        5. Herhangi bir hata oluşursa loglara yazar.

    """
    try:
        cur = conn.cursor()

        check_query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='{table_name}') AS table_existence"
        
        cur.execute(check_query)

        result = cur.fetchall()
        result=result[0][0]
        
        if result == True and sayac==0:
           
            delete_query=f"drop table {table_name}"
            cur.execute(delete_query)
            conn.commit()
            
        columns = csv_df.columns
        columns_definition = ""

        for col in columns:
            columns_definition += f"{col} INTEGER, "

        columns_definition = columns_definition.rstrip(", ")
        create_table_query = f"CREATE TABLE {table_name} ({columns_definition});"
        
        cur.execute(create_table_query)
        conn.commit()

        logging.info(f"Table named {table_name} append to database successfully")

    except Exception as e:
        logging.error(f"create_table - {e}")

def insert_data(table_name,csv_df):
    """
    Bu fonksiyon, CSV'deki verileri PostgreSQL tablosuna ekler.

    Parametreler:
        table_name: Verilerin ekleneceği tablonun adı (string).
        csv_df: Eklenecek verileri içeren pandas DataFrame.

    Yaptığı İşlemler:
        1. Veritabanına bağlanır.
        2. CSV'deki her bir satırı tabloya ekler.
        3. Hataları loglara yazar.

    """
    conn = connect_db()
    cur = conn.cursor()
    columns = ", ".join(csv_df.columns)

    try:
        for index, row in csv_df.iterrows():
            values = ""
            for val in row:
                values += f"'{val}', "
            values = values.rstrip(", ")
            
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            cur.execute(insert_query)
            conn.commit()
       
        logging.info(f"Data successfully added to {table_name} table.")
    except Exception as e:
            logging.error(f"insert_data - {e}")

def get_data_from_db(conn, table_name):
    """
    Bu fonksiyon, belirtilen PostgreSQL tablosundan veriyi çeker ve bir pandas DataFrame olarak döner.

    Parametreler:
        conn: Veritabanı bağlantı nesnesi.
        table_name: Verilerin çekileceği tablonun adı.

    Return:
        db_dataframe: Çekilen verileri içeren pandas DataFrame.

    Yaptığı İşlemler:
        1. Tablodan tüm veriyi çeker.
        2. Veriyi pandas DataFrame'e dönüştürür.
        3. Hataları loglara yazar.

    """
    try:
        query = f"SELECT * FROM {table_name};"  
        db_dataframe = pd.read_sql_query(query, conn)

        logging.info(f"Data was successfully retrieved from the database.")
    
        return db_dataframe
        
    except Exception as e:
        logging.error(f"get_data_from_db - {e}")
    
def setup_logging(log_file=config.LOG_FILE,level=logging.INFO):
    """
    Bu fonksiyon, loglama ayarlarını yapılandırır.

    Parametreler:
        log_file: Logların kaydedileceği dosyanın yolu (varsayılan config.LOG_FILE).
        level: Loglama seviyesi (varsayılan INFO).

    Yaptığı İşlemler:
        1. Loglama ayarlarını yapılandırır (log dosyası, seviye, format vb.).
    
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S", 
    )

