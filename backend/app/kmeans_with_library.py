import warnings
import time
import logging

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from app.save_result import save_results
       
def normalize_data(dataframe):
    """
    Bu fonksiyon, verilen veri setindeki değerleri MinMaxScaler kullanarak 0 ile 1 arasına ölçeklendirir. 

    Parametreler:
    df: Normalize edilecek veri seti. Veri çerçevesi, sayısal sütunlar içermelidir.

    Return Değeri:
    scaler_fit: Normalize edilmiş veri seti. 0 ile 1 arasında değerler içeren bir numpy dizisi döndürür. 
    
    """
    try:
        scaler = MinMaxScaler()
        scaler_fit=scaler.fit_transform(dataframe)
        return scaler_fit 
    except Exception as e:
        logging.error(f"with_library file -> normalize_data func - {e}")

def find_best_value_kmeans(scaled_data, cluster,n_init=10):
    """
    KMeans algoritması kullanarak en iyi küme sayısını bulur.

    Parametreler:
    scaled_data (ndarray veya DataFrame): KMeans algoritması için ölçeklendirilmiş veri seti.
    cluster (int): Denenecek maksimum küme sayısı.

    Return Değerleri:
    best_k: En iyi küme sayısı.
    best_value: En yüksek Silhouette skoru.
    best_model: En başarılı KMeans modeli.

    Bu fonksiyon, verilen ölçeklendirilmiş veri seti üzerinde KMeans algoritmasını 
    uygular ve en yüksek Silhouette skoruna sahip küme sayısını belirler. 
    
    """
    try:
        best_value = -1
        best_k = 1
        for k in range(2, cluster + 1):
            kmeans = KMeans(n_clusters=k, random_state=42,n_init=10)
            labels = kmeans.fit_predict(scaled_data)
            value = silhouette_score(scaled_data, labels)
            if value > best_value:
                best_value = value
                best_k = k
                best_model = kmeans
        
        return  best_k,best_value,best_model
    
    except Exception as e:
        logging.error(f"with_library file -> find_best_value_kmeans func - {e}")
        
def main(dataframe,max_cluster_num):
    """
    Kod akışını yöneten fonksiyon.
    Sırasıyla İşlevi:
    - Veritabanına bağlanır.
    - Verileri alır.
    - Verileri normalize eder.
    - KMeans algoritmasını kullanarak en iyi küme sayısını bulur.
    - Sonuçları bir CSV dosyasına kaydeder.
    - İşlem süresini kaydeder.
    
    Hata durumunda, hata kaydı oluşturur.

    """
    warnings.filterwarnings("ignore")

    # timer başlangıç
    start_time = time.time()

    # Normalizasyon
    scaled_data = normalize_data(dataframe)

    # En uygun küme sayısını bul    
    best_k, score, best_model_kmeans = find_best_value_kmeans(scaled_data, max_cluster_num)
    dataframe["output"] = best_model_kmeans.labels_
    
    #timer bitiş
    end_time = time.time()

    execution_time = end_time - start_time

    # Sonuçları yazdır.
    save_results(dataframe, execution_time, best_k, score,"Library",first_call=True)

    logging.info("K means with library version completed successfully.")

    return dataframe,['{:.5f}'.format(execution_time),best_k,'{:.5}'.format(score)]

if __name__ == "__main__":  
    main()
