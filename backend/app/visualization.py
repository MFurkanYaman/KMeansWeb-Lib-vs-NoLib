import logging
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

from app import config


def visualize_with_library(df1,table_name):
    """
    Kütüphane kullanarak verilen veri çerçevesinin PCA görselleştirmesini oluşturur.
    
    Parametreler:
        - df1: Görselleştirilecek dataframe.
        - table_name: Görselin kaydedileceği dosya adı için kullanılacak tablo ismi.

    Yaptığı İşlemler:
        1. 'output' sütununu çıkararak PCA için veriyi hazırlar.
        2. PCA uygulayarak iki bileşen elde eder.
        3. Sonuçları bir scatter plot ile görselleştirir.
        4. Grafiği belirtilen dosya yoluna kaydeder.

    Return:
        - Görselin dosya yolu (img_path).

    """
    try:
        #Grafik ismini ve yolunu dinamik olarak belirleme
        img_name = table_name+"_library.png"
       
        img_path = Path(config.IMG_FOLDER) / img_name
        img_path.parent.mkdir(parents=True, exist_ok=True)

        df_pca=df1.drop("output", axis=1)
      
        #PCA ile boyut indirgeme işlemi
        pca = PCA(n_components=2)
        pca_fit=pca.fit_transform(df_pca)
      
        #Grafik yazma işlemi
        plt.figure(figsize=(10,12))
        plt.scatter(pca_fit[:, 0], pca_fit[:, 1], c=df1["output"], cmap='viridis')
        plt.title("Results of Using Library")  
        

        #Grafiği belirtilen yola kaydetme işlemi
        plt.savefig(img_path)

        

     

        return img_path
    
    except Exception as e:
        logging.error(f"visualize_with_library -> {e}")

def visualize_without_library(df2,table_name):
    """
    Kütüphane olmadan verilen veri çerçevesinin PCA görselleştirmesini oluşturur.
    
    Parametreler:
        - df2: Görselleştirilecek dataframe.
        - table_name: Görselin kaydedileceği dosya adı için kullanılacak tablo ismi.

    Yaptığı İşlemler:
        1. 'output' sütununu çıkararak PCA için veriyi hazırlar.
        2. PCA uygulayarak iki bileşen elde eder.
        3. Sonuçları bir scatter plot ile görselleştirir.
        4. Grafiği belirtilen dosya yoluna kaydeder.

    Return:
        - Görselin dosya yolu (img_path).
    
    """
    try:
        #Grafik ismini ve yolunu dinamik olarak belirleme
        img_name = table_name+"_without_library.png"
        img_path = Path(config.IMG_FOLDER) / img_name
        img_path.parent.mkdir(parents=True, exist_ok=True)
        
        #PCA ile boyut indirgeme işlemi
        df_pca=df2.drop("output", axis=1)
        pca = PCA(n_components=2)
        pca_fit=pca.fit_transform(df_pca)
        
        #Grafik yazma işlemi
        plt.figure(figsize=(10, 12))
        plt.scatter(pca_fit[:, 0], pca_fit[:, 1], c=df2["output"], cmap='viridis')
        plt.title("Results of Without Library")

        #Grafiği belirtilen yola kaydetme işlemi
        plt.savefig(img_path)

        #Front-end'e gönderilen yol.
        

        return img_path
    
    except Exception as e:
        logging.error(f"visualize_without_library -> {e}")

