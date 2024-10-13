import unittest
import numpy as np
import pandas as pd
from app.kmeans_with_library import find_best_value_kmeans, normalize_data


class TestKMeans(unittest.TestCase):

    def example_dataset(self):

        """
        Testler için gerekli başlangıç verisini hazırlar.
        """
       
        np.random.seed(42)  
        self.data = np.random.rand(10, 3)  # 100 satır ve 3 özellik
        self.df = pd.DataFrame(self.data, columns=['Feature_1', 'Feature_2', 'Feature_3'])

    def test_find_best_value_kmeans(self):
        """
        KMeans algoritması için en uygun küme sayısını bulma fonksiyonunu test eder.
        """
        # Veriyi normalize et
        scaled_data = normalize_data(self.df)

        # KMeans için en uygun küme sayısını bul (5 küme denenecek)
        best_k, best_value, best_model = find_best_value_kmeans(scaled_data, cluster=5,n_init=10)

        # Beklenen sonuçlar
        self.assertTrue(1 <= best_k <= 5, "Best k 1 ve 5 arası olmalı.")
        
        # Silhouette skoru 0 ile 1 arasında olmalı
        self.assertTrue(0 <= best_value <= 1, "Silhouette score 0-1 arasında olmalı")

        # Kontrol: modelin n_clusters parametresi en iyi küme sayısına eşit olmalı
        self.assertEqual(best_model.n_clusters, best_k, "modelin n_clusters parametresi en iyi küme sayısına eşit olmalı")

if __name__ == '__main__':
    unittest.main()
