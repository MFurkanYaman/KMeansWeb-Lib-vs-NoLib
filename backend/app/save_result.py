import pandas as pd
import logging

from app import config

def save_results(dataframe,execution_time,best_k,score,method,first_call):
    """
    Sonuçları CSV dosyasına kaydeder.

    Parametreler:
    dataframe: KMeans algoritması ile elde edilen verileri içeren DataFrame.
    execution_time: Algoritmanın çalışma süresi (saniye cinsinden).
    best_k: En iyi küme sayısı.
    score: KMeans algoritması için hesaplanan Silhouette skoru.
    method: 'With Library' veya 'Without Library' gibi metodu belirten dinamik metin.

    Bu fonksiyon, verilen DataFrame ve performans metriklerini kullanarak 
    'static/results/result.csv' dosyasına sonuçları kaydeder. Çalışma süresi ve Silhouette skoru 
    gibi performans metriklerinin yalnızca ilk altı hanesi kaydedilir.
    """    
    try:
        result_file=config.RESULT_FILE
        if first_call==True:  # Eğer ilk çağrı ise eski dosyanın içeriğini sil.
            open(result_file, 'w').close()

        results_summary = pd.DataFrame({
                "Method": [method],  # Dinamik olarak yöntemi belirtiyor
                "Execution Time (s)": [str(execution_time)[:6]],  
                "Best K": [best_k],
                "Silhouette Score": [str(score)[:6]]  
            }) 

        empty_df = pd.DataFrame() #Dosya karışıklığını engellemek için boş bir df üret.

        #Sonucu kaydet
        empty_df.to_csv(result_file, mode="a", index=False)
        results_summary.to_csv(result_file, mode="a", index=False)
        dataframe.to_csv(result_file, mode="a", index=False)

    except Exception as e:
        logging.error(f"save_results function -> {e}")

