import unittest
import numpy as np
import pandas as pd
from app.kmeans_without_library import calculate_distance, kmeans_func, calculate_silhoutte_score


class TestKMeans(unittest.TestCase):

    def test_dataset(self):
        """ Test amaçlı veri seti oluşturur."""
        np.random.seed(42)  
        self.data = np.random.rand(10, 3)  
        self.df = pd.DataFrame(self.data, columns=['Feature_1', 'Feature_2', 'Feature_3'])

    def test_calculate_distance(self):
        """ Uzaklık hesaplama algoritmasının çalıştığını kontrol eder."""
        centroids = np.array([[0.5, 0.5, 0.5]])
        distance_dict = calculate_distance(self.data, centroids, centroids_num=1)
        self.assertEqual(len(distance_dict[0]), 10)  

    def test_kmeans_func(self):
        """K-means algoritmasının çalıştığını kontrol eder."""
        centroids = self.data[:2]  
        clusters = kmeans_func(self.data, centroids, centroids_num=2)
        # İki küme olup olmadığını kontrol et
        self.assertEqual(len(clusters), 2)

    def test_calculate_silhoutte_score(self):
        """Silhouette skorunu hesaplayan fonksiyonun çalıştığını kontrol eder."""
        self.df["output"] = [0, 0, 1, 1, 0, 1, 1, 0, 1, 0]  
        score = calculate_silhoutte_score(self.df, centroids_num=2)
        # Skorun -1 ile 1 arasında olup olmadığını kontrol et
        self.assertTrue(-1 <= score <= 1)



if __name__ == '__main__':
    unittest.main()
