import time
import copy
import warnings
import logging
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

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
        logging.error(f"normalize_data-{e}")

def calculate_distance(data, centroids, centroids_num):
    """
    Veri noktaları ile merkezler arasındaki uzaklığı Öklid yöntemiyle hesaplar.

    Parametreler:
    data: Numpy array, veri noktaları.
    centroids: Numpy array, küme merkezleri.
    centroids_num: int, merkez sayısı.

    Return:
    distance_dict: Sözlük formatında, her merkez için tüm veri noktalarına olan uzaklıkları içerir.
    
    """
    try:
        distance_dict = {}
        for i in range(centroids_num):
            distances = []
            for j in range(len(data)):
                distance = np.sqrt(np.sum((data[j] - centroids[i])**2))
                distances.append(distance)
            distance_dict[i] = distances
        return distance_dict
    except Exception as e:
        logging.error(f"calculate_data-{e}")

def find_clusters(distance_dict, row_num, centroids_num):
    """
    Veri noktalarını merkezlerle olan mesafelerine göre en yakın kümeye atar.

    Parametreler:
    distance_dict: Her bir merkez için veri noktalarına olan mesafeleri içeren sözlük.
    row_num: Veri setindeki satır sayısı.
    centroids_num: Merkezlerin sayısı (kümelerin sayısı).
    clusters: Sözlük olarak her bir merkez için, o merkeze atanmış veri noktalarının
              indekslerini içeren kümeler  döndürür.

    Return :
    clusters: Sözlük olarak, her bir merkez için o merkeze atanmış veri noktalarının indekslerini içerir.
    return şekli örneği: {1: [0, 1, 3, 5, 8, 13, 14, 15, 16, 18], 0: [2, 4, 6, 7, 9, 10, 11, 12, 17, 19]}
    
    """
    try:
        clusters = {}
        for i in range(row_num):
            min_value = float("inf")
            for j in range(centroids_num):
                if distance_dict[j][i] < min_value:
                    min_value = distance_dict[j][i]
                    min_key = j
            if min_key not in clusters:
                clusters[min_key] = []
            clusters[min_key].append(i)
        return clusters
    except Exception as e:
        logging.error(f"find_cluster-{e}")

def update_centroids(data, clusters, centroids_num):
    """
    Kümelerdeki veri noktalarına göre merkezleri (Centroids) günceller.Kümeler belirlendikten sonra 
    her bir kümenin merkez noktası, kümeye atanmış veri noktalarının
    ortalaması olarak yeniden hesaplanır.

    Parametreler:
    data: Numpy array, normalleştirilmiş data.
    clusters: Sözlük, kümelere atanmış veri noktalarının indekslerini içerir.
    centroids_num: int, merkez sayısı.

    Return :
    new_centroids: Numpy array, her küme için yeni merkez konumları.
    return şekli örneği: [[0.74561404 0.62943262 0.58333333 0.71477663]
                         [0.39473684 0.34878419 0.50531915 0.38586156]]
    
    """
    try:
        new_centroids_list = []

        for i in range(centroids_num):    
            total = np.zeros(data.shape[1], dtype=np.float64)
            for inside_value in clusters[i]:
                total += data[inside_value]
            new_centroid = total / len(clusters[i])
            new_centroids_list.append(new_centroid)

        return np.array(new_centroids_list)
    
    except Exception as e:
        logging.error(f"update_centroids-{e}")

def kmeans_func(data, centroids, centroids_num):
    """
    K-means algoritmasının ana fonksiyonu. K-means algoritması, merkezler güncellenene kadar iteratif bir süreçte çalışır. 
    Her iterasyonda veri noktaları en yakın merkeze atanır ve merkezler güncellenir.Kümeleme işlemini gerçekleştirir.

    Parametreler:
    data: Numpy array, normalleştirilmiş veri seti.
    centroids: Numpy array, başlangıç merkezleri.
    centroids_num: int, centroids sayısı (kümelerin sayısı).

    Return :
    clusters: K-means algoritmasının son çıktısı, her bir veri noktası için küme atamalarını içerir.    
    
    """
    try:
        row_num = data.shape[0]
        old_clusters={}

        for i in range(centroids_num):
            old_clusters[i]= []

        while True:

            distance_dict = calculate_distance(data, centroids, centroids_num)
            clusters = find_clusters(distance_dict, row_num, centroids_num)
            centroids = update_centroids(data, clusters, centroids_num)
 
            if clusters==old_clusters:
                break
            else:
                old_clusters = copy.deepcopy(clusters)
 
        return clusters
 
    except Exception as e:
        logging.error(f"kmeans_func-{e}")



def calculate_a_values(dataframe, centroids_num):
    """
    Aynı küme içindeki noktaların birbirine olan ortalama mesafesini (a(i) değeri) hesaplar.

    Parametreler:
    dataframe: Pandas DataFrame, küme atamaları yapılmış veri.
    centroids_num: int, küme sayısı.

    Return :
    centroids_a_value: Her küme için a(i) değerini içeren sözlük.
    """

    try:
        centroids_a_value = {}
        original_df_len = dataframe.shape[1] - 1  # Output kolonunu çıkartıyoruz.
        scaled_data = pd.DataFrame(normalize_data(dataframe.iloc[:, :original_df_len]), columns=dataframe.columns[:original_df_len])
        scaled_data = pd.concat([scaled_data, dataframe.iloc[:, -1]], axis=1)

        for i in range(centroids_num):
            total_a_mean = 0
            clusters = scaled_data[scaled_data["output"] == i].drop(columns=["output"])  
            for j in range(len(clusters)):
                distances_a = []
                for k in range(len(clusters)):
                    if j != k:  # Kendisi ile mesafeyi hesaplamıyoruz.
                        distance_a = np.sqrt(np.sum((clusters.iloc[j].values - clusters.iloc[k].values) ** 2))
                        distances_a.append(distance_a)
                a_mean = np.mean(distances_a)
                total_a_mean += a_mean
            total_a_mean /= len(clusters)
            centroids_a_value[i] = total_a_mean
        
        return centroids_a_value
    
    except Exception as e:
        logging.error(f"calculate_a_values-{e}")

def calculate_b_values(dataframe, centroids_num):
    """
    Farklı kümelerdeki noktalar arasındaki ortalama mesafeleri (b(i) değeri) hesaplar.

    Parametreler:
    dataframe: Pandas DataFrame, küme atamaları yapılmış veri.
    centroids_num: int, küme sayısı.

    Return :
    same_group: Her küme için b(i) değerlerini içeren sözlük.
    
    """
    try:
        centroids_b_value = {}
        original_df_len = dataframe.shape[1] - 1  # Output kolonunu çıkartıyoruz.
        scaled_data = pd.DataFrame(normalize_data(dataframe.iloc[:, :original_df_len]), columns=dataframe.columns[:original_df_len])
        # print(dataframe)
        # print(scaled_data)
        scaled_data = pd.concat([scaled_data, dataframe.iloc[:, -1]], axis=1)
        # print(scaled_data)
        
        for i in range(centroids_num):
            clusters = scaled_data[scaled_data["output"] == i].drop(columns=["output"])
            for j in range(len(clusters)):  
                min_b_mean = float("inf")  
                for k in range(centroids_num):  
                    if i != k:  
                        other_clusters = scaled_data[scaled_data["output"] == k].drop(columns=["output"])
                        distances_b = []
                        for m in range(len(other_clusters)):
                            distance_b = np.sqrt(np.sum((clusters.iloc[j].values - other_clusters.iloc[m].values) ** 2))
                            distances_b.append(distance_b)
                        b_mean = np.mean(distances_b)  # O diğer kümedeki noktalarla olan ortalama mesafe
                        if b_mean < min_b_mean:  # En küçük ortalama mesafeyi al
                            min_b_mean = b_mean
                centroids_b_value[(i, j)] = min_b_mean
        
        # b değerlerini kümelerine göre gruplandır
        same_group = {}
        for (cluster_label, index), distance in centroids_b_value.items():
            if cluster_label not in same_group:
                same_group[cluster_label] = []
            same_group[cluster_label].append(distance)
        
        # b ortalamasını bul
        for cluster_label, distances in same_group.items():
            if len(distances) > 0:
                mean_total_b = sum(distances) / len(distances)
                same_group[cluster_label] = mean_total_b
            else:
                same_group[cluster_label] = None
        
        return same_group
    except Exception as e:
        logging.error(f"calculate_b_values-{e}")

def calculate_silhouette_score(centroids_a_value, same_group, centroids_num):
    """
    Gelen a skor ve b skor verilerini kullanrak silhoutte score hesaplar.

    Return: 
    score_mean: Her veri grubu için ortalama silhoutte score değeridir.

    """
    try:
        score = []
        for i in range(centroids_num):
            if np.isnan(centroids_a_value[i]) or np.isnan(same_group[i]):
                continue
            else:
                score.append((same_group[i] - centroids_a_value[i]) / max(same_group[i], centroids_a_value[i]))
        score_mean = np.mean(score)
        return score_mean
    except Exception as e:
        logging.error(f"calculate_silhouette_score -> {e}")

def silhoutte_function(dataframe, centroids_num):
    """
    Veri gruplarının silhoutte score değerlerini hesaplamasını sağlayan 
    yapının modülre bir şekilde çalışmasını sağlar.
    """
    try:
        centroids_a_value = calculate_a_values(dataframe, centroids_num)
        same_group = calculate_b_values(dataframe, centroids_num)
        score_mean = calculate_silhouette_score(centroids_a_value, same_group, centroids_num)
        return score_mean
    except Exception as e:
        logging.error(f"silhoutte_function -> {e}")

    
def main(dataframe,max_cluster_num):
    """
    Verilen bir dataframe üzerinde kütüphane kulalnmadan K-Means kümeleme işlemi yapan ana fonksiyon.
    Bu fonksiyon veriyi normalize eder, farklı küme sayıları için K-Means algoritmasını çalıştırır,
    her kümeleme sonucu için silhoutte skorunu hesaplar ve en iyi skora sahip olan kümeleme çözümünü döner.
    Ayrıca kümeleme işlemi süresince geçen zamanı kaydeder ve sonuçları kaydeder.

    Parametreler:
        dataframe: Kümeleme yapılacak veri seti.
        max_cluster_num (int): Denenecek maksimum küme sayısı.

    Return:
        best_df: En iyi kümeleme sonucuna sahip dataframe.
        summary (list): Çalışma süresi, en iyi küme sayısı ve en iyi silhoutte skorunu içeren liste.

    Adımlar:
        1. Giriş veri setini normalize eder.
        2. 2'den max_cluster_num'a kadar her bir küme sayısı için:
           - Normalize edilmiş veriden rastgele başlangıç merkezleri (centroid) seçer.
           - Seçilen merkezlerle K-Means algoritmasını çalıştırır.
           - Küme etiketlerini orijinal veriye atar.
           - Kümeleme sonucu için silhoutte skorunu hesaplar.
        3. En yüksek silhoutte skoruna sahip küme sayısını bulur ve o skora sahip küme sayısı 
           en iyi küme sayısı olarak seçilir.
        4. Kümeleme sonuçlarını ve çalışma süresini kaydeder.
        5. Küme etiketlerine sahip en iyi dataframe'i ve sonuç özetini döner.
    """
    
    try:
        warnings.filterwarnings("ignore")

        start_time = time.time()

        # Normalizasyon
        scaled_data = normalize_data(dataframe)
        
        score_dict={}
        df_dict={}
        
        # Küme döngüsü sağlar
        for centroids_num in range (2,max_cluster_num+1):

            #Scaled data içerisinden seçilen rastgele centroids_num kadar veri noktası centroids olur.
            random_indices = np.random.choice(scaled_data.shape[0], centroids_num, replace=False) #rastgele indis seçti
            first_centroids = scaled_data[random_indices, :]  #seçilen indisleri aldı ve scaled data dan çekti.
     
            # K-Means 
            final_clusters = kmeans_func(scaled_data, first_centroids, centroids_num)

            temp_df = dataframe.copy()
            temp_df["output"] = -1
                    
            for cluster_label, index in final_clusters.items():
                temp_df.loc[index, "output"] = cluster_label # indexte cluster labelsı atar
            
            silhoutte_score=silhoutte_function(temp_df,centroids_num)
            score_dict[centroids_num]=silhoutte_score
            df_dict[centroids_num] = temp_df

        best_centroids_num = max(score_dict, key=score_dict.get)
        best_df = df_dict[best_centroids_num]
    
        end_time = time.time()
        execution_time = end_time - start_time
        save_results(best_df, execution_time, best_centroids_num, score_dict[best_centroids_num],"Without Library",first_call=False)

        logging.info("K means without library version completed successfully.")

        return best_df,['{:.5f}'.format(execution_time),best_centroids_num,'{:.5f}'.format(score_dict[best_centroids_num])]
    
    except Exception as e:
        logging.error(f"K-means without library main function -> {e}")

if __name__ == "__main__":
    main()
