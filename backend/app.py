import os
import logging

import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from app import config
from app import kmeans_with_library
from app import kmeans_without_library
from app import db_operations
from app import visualization

app = Flask(__name__)
CORS(app)

# Veri yolları
upload_folder = config.UPLOADER_FOLDER
image_folder = config.IMG_FOLDER
result_path=config.RESULT_FILE


@app.route("/", methods=["GET", "POST"])

def run_algorithm():
    """
    Bu fonksiyon, kullanıcıdan alınan veri dosyasını ve küme sayısını kullanarak KMeans algoritmasını
    iki farklı yöntemle çalıştırır. Veriler önce veritabanına eklenir, sonra KMeans sonuçları elde edilir.
    
    Parametreler:
        - file: Kullanıcıdan yüklenen CSV dosyası.
        - cluster_num: Kullanıcının belirttiği maksimum küme sayısı (form alanı ile gelir).

    Yaptığı İşlemler:
        1. CSV dosyasını yükleyip kaydeder.
        2. "id" kolonlarını veriden çıkarır.
        3. Veriyi veritabanına ekler.
        4. KMeans algoritmalarını iki farklı yöntemle çalıştırır (kütüphane ile ve kütüphane olmadan).
        5. Sonuçları görselleştirir ve grafikleri dosyaya kaydeder.

    Return:
        - JSON formatında başarı mesajı döner.
        - Hatalı durumlarda loglara hata yazılır ve hata mesajı döner.

    """
    try:

        global result_list_lib, result_list_unlib,img1_path,img2_path
        
        #Kullanıcıdan veri setini alır.
        file = request.files["file"]
        data_path = os.path.join(upload_folder, file.filename)
        file.save(data_path) 

        #Kullanıcıdan küme sayısını alır.
        max_cluster_num = int(request.form.get("cluster_num"))

        #Logging ayarlarını atama işlemi
        db_operations.setup_logging()
        
        # Veriyi oku
        csv_df = pd.read_csv(data_path)

        # Veri setinde id var ise drop et.
        for column in csv_df.columns:
                if "id" in column.lower():
                    csv_df=csv_df.drop(column,axis=1)
        
        # Tablo ismini belirle
        table_name = os.path.splitext(os.path.basename(data_path))[0]
        table_name=table_name.lower() #veri tabanına küçük isimle kayıt
        
        # Veritabanı bağlantısını kur
        conn = db_operations.connect_db()

        # Tabloyu oluştur
        db_operations.create_table(table_name, conn, csv_df)

        # Verileri veritabanına ekle
        db_operations.insert_data(table_name, csv_df)

        # Verileri veritabanından çek
        dataframe = db_operations.get_data_from_db(conn, table_name)

        # KMeans işlemlerini çalıştır
        df1,result_list_lib = kmeans_with_library.main(dataframe, max_cluster_num)
        df2,result_list_unlib = kmeans_without_library.main(dataframe, max_cluster_num)
        
        # Grafik çıktıya çevir
        img1_path = visualization.visualize_with_library(df1,table_name)
        img2_path=  visualization.visualize_without_library(df2,table_name)
        
        logging.info("The algorithm successfully executed.")

        return jsonify({"Message":"The algorithm successfully executed."        
                    }), 200
    except Exception as e:
        logging.error(f"run_algorithm -> {e} ")
        return jsonify({"Error":f"{e}"})


@app.route("/get_image", methods=["GET"])
def get_image():
    """
    Bu fonksiyon, KMeans algoritmasının sonuçlarına göre oluşturulan grafiklerin yollarını döner.
    
    Return:
        - JSON formatında img1 ve img2 adında görsel yolları döner.
        - Hatalı durumlarda loglara hata yazılır ve hata mesajı döner.

    """       
    try:
        return jsonify({"img1": f"{img1_path}"},  #başka bir çözüm yolu var mı ?
                    {"img2": f"{img2_path}"}), 200 
    except Exception as e:
        logging.error(f"get_image -> {e}")
    
@app.route("/download_csv", methods=["GET"])
def download_csv_file():
    """
    Bu fonksiyon, kullanıcıya sonuç dosyasını indirme imkanı sunar.
    
    Return:
        - CSV dosyasını indirilebilir hale getirir.
        - Hatalı durumlarda loglara hata yazılır ve hata mesajı döner.

    """
    try:
        return send_file(f"{result_path}", as_attachment=True,mimetype='text/csv')
    except Exception as e:
        logging.error(f"download_csv_file -> {e}")
        return jsonify({"Error":f"{e}"})

@app.route("/get_results", methods=["GET"])
def get_results():
    """
    Bu fonksiyon, KMeans algoritması sonuçlarını kullanıcıya dönürür.
    
    Return:
        - JSON formatında, kütüphane ile ve kütüphane olmadan elde edilen KMeans sonuçlarını döner.
        - Hatalı durumlarda loglara hata yazılır ve hata mesajı döner.

    """
    try:
        return jsonify({
            "value1": result_list_lib,
            "value2": result_list_unlib
        }), 200
    except Exception as e:
        logging.error(f"get_results -> {e}")
        return jsonify({"Error":f"{e}"})
         


if __name__ == "__main__":
    app.run(debug=True)
