# KMeansWeb-Lib-vs-NoLib

# Türkçe

**The English version of this README file is provided below.**

Bu proje, Python kullanılarak geliştirilen bir web uygulamasıdır. Uygulama, K-Means algoritmasını hem kütüphane kullanarak hem de kütüphane kullanmadan çalıştırır. Sonuçlar, Silhouette Skoru ile kıyaslanarak en iyi küme sayısı belirlenir. Ayrıca, proje PostgreSQL kullanılarak veritabanına veri aktarımı, loglama, ve Flask ile metodların servis edilmesini içerir. Bu README dosyasında proje hakkında detaylı bilgi verilmektedir.

## Uygulama Ekran Görüntüleri / Application Screenshots

1. **Giriş ve Dosya Yükleme Arayüzü / Application Interface and File Upload**:
   ![Giriş ve Dosya Yükleme](images/ApplicationInterfaceScreen.PNG)

2. **Dosya Yükleme İşlemi / File Upload Process**:
   ![Dosya Yükleme İşlemi](images/UploadResultSection.PNG)

3. **Sonuçların CSV Olarak İndirilmesi ve Kıyaslanması / Downloading CSV and Comparing Results**:
   ![Sonuçları İndirme ve Kıyaslama](images/DisplayResult.png)

   
  

## Proje İçeriği

- **PostgreSQL**: Veriler, PostgreSQL veritabanına aktarılır ve uygulama bu verileri veritabanından tüketir.
- **K-Means Algoritması**: Kütüphane kullanarak ve kullanmadan iki farklı yöntemle K-Means algoritması uygulanmıştır. Sonuçlar karşılaştırılarak model performansı analiz edilmiştir.
- **PCA (Principal Component Analysis)**: Kümeleme işlemi öncesinde boyut indirgeme işlemi olarak PCA kullanılmıştır.
- **Silhouette Skoru**: Kümeleme performansını ölçmek için Silhouette skoru kullanılmıştır.
- **Sonuçları İndirme**: Uygulama, kümeleme işleminin sonuçlarını `.csv` formatında indirmenize olanak tanır.
- **Loglama**: Uygulama içerisinde meydana gelen işlemler ve hatalar loglanarak kaydedilmiştir.
- **Flask ile Servis Edilen Metodlar**: Uygulama, Flask framework'ü kullanarak servis edilen metodlar içerir.
- **Unit Testler**: Her bir metod için birim testler geliştirilmiştir.

## K-Means Algoritması

### K-Means Algoritması Nedir?

K-Means, denetimsiz öğrenme yöntemlerinden biri olan kümeleme algoritmaları arasında en popüler olanıdır. Bu algoritma, bir veri setini belirli sayıda kümeye ayırarak, her bir kümeye en yakın veri noktalarını gruplamayı amaçlar. Algoritmanın temel amacı, verileri kümelere ayırmaktır.

### K-Means Algoritmasının Çalışma Adımları

1. **Kümelerin Sayısının Belirlenmesi (K değeri)**:
    Kullanıcı tarafından önceden belirlenen K değeri, veri setindeki denenecek maksimum küme sayısını belirler.

2. **Başlangıç Merkezlerinin Rastgele Seçilmesi**:
    Algoritma, verilerin merkezine yakın rastgele K adet merkezi başlangıç noktası olarak seçer.

3. **Her Noktanın En Yakın Merkeze Atanması**:
    Her bir veri noktası, en yakın olduğu merkez ile ilişkilendirilir ve o merkezin kümesine dahil edilir. Mesafe ölçütü olarak  Öklid (Euclidean) mesafesi kullanılır.

4. **Merkezlerin Güncellenmesi**:
    Her bir kümedeki veri noktalarının ortalaması alınarak, yeni kümelerin merkezleri hesaplanır. Bu işlem, kümelerin daha iyi tanımlanmasına yardımcı olur.

5. **Tekrar Atama ve Güncelleme**:
    Veri noktaları, yeni merkezlere göre tekrar atanır ve adımlar 3 ve 4, küme merkezleri artık değişmeyene kadar tekrarlanır.

6. **Algoritmanın Sonlanması**:
    Küme merkezleri sabit kaldığında algoritma sonlanır.

### Örnek:
Bir K-Means algoritması uygulandığında, 2 boyutlu bir veri seti şu şekilde çalışır:
- Başlangıçta 3 küme (K = 3) belirlenmiştir.
- Algoritma, veri noktalarını 3 rastgele merkez etrafında gruplar ve her iterasyonda bu merkezleri güncelleyerek en yakın ve en optimum kümeyi bulur.

### Kütüphane Kullanmadan Uygulanan K-Means
Projede K-Means algoritması sıfırdan yazılarak, kütüphane kullanılmadan uygulanmıştır. Algoritmanın her adımı manuel olarak kodlanmış ve verilerin kümelenmesi sağlanmıştır.

### Kütüphane Kullanarak Uygulanan K-Means
Alternatif olarak, `scikit-learn` kütüphanesi kullanılarak daha optimize bir K-Means çözümü sağlanmıştır. `scikit-learn`, K-Means algoritmasını hızlı bir şekilde uygulamak ve sonuçları analiz etmek için popüler bir Python kütüphanesidir.


### PCA (Principal Component Analysis)
Kümeleme algoritmasını çalıştırmadan önce, verilerin boyutunu düşürmek amacıyla PCA kullanılmıştır. PCA, yüksek boyutlu verileri iki ya da üç boyuta indirger ve böylece verilerin daha anlamlı hale gelmesini sağlar.

### Silhouette Skoru Nedir?

Silhouette skoru, bir kümeleme modelinin ne kadar iyi performans gösterdiğini ölçen bir metriktir. Her bir veri noktası için şu şekilde hesaplanır:

$$
\text{Silhouette Skoru} = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

- **a(i)**: Veri noktası ile aynı kümedeki diğer noktalar arasındaki ortalama mesafe.
- **b(i)**: Veri noktası ile en yakın diğer kümedeki noktalar arasındaki ortalama mesafe.

Silhouette skoru, -1 ile 1 arasında bir değer alır. 1’e yakın skorlar iyi bir kümelenme performansını gösterirken, 0’a yakın skorlar, veri noktalarının kümeler arasında eşit uzaklıkta olduğunu, yani kararsız olduğunu gösterir. Negatif skorlar ise veri noktalarının yanlış kümelendiğini işaret eder.

## Loglama

Proje boyunca meydana gelen işlemler ve olası hatalar, loglama sistemi ile kayıt altına alınmıştır. Bu sayede hatalar izlenebilir ve çözümler üretilebilir.

## Flask API

Bu projede, Flask kullanılarak geliştirilen metodlar API olarak sunulmaktadır. Uygulama, veritabanı işlemleri, K-Means algoritması ve loglama gibi fonksiyonları bu API üzerinden çalıştırır.


## Unit Testler

Her bir metod için birim testler geliştirilmiştir. Testler, uygulamanın beklenilen şekilde çalışıp çalışmadığını doğrular.

## Kurulum

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları izleyin:

### Gereksinimler
- Python
- PostgreSQL
- Flask
- React
- Docker (opsiyonel)


### Adımlar

1. **Depoyu klonlayın**:
    ```bash
    git clone https://github.com/MFurkanYaman/KMeansWeb-Lib-vs-NoLib.git
    cd KMeansWeb-Lib-vs-NoLib
    ```

2. **Gereksinimleri yükleyin**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Uygulamayı çalıştırın**:
    ```bash
    flask run
    ```

5. **Frontend (React) kurulum ve çalıştırma**:
    ```bash
    cd frontend
    npm install
    npm start
    ```


# English
This project is a web application developed using Python. The application runs the K-Means algorithm both with and without libraries. The results are compared using the Silhouette Score to determine the best number of clusters. Additionally, the project includes data transfer to a PostgreSQL database, logging, and serving methods using Flask. This README file provides detailed information about the project.

## Project Contents

- **PostgreSQL**: Data is transferred to a PostgreSQL database, and the application consumes this data from the database.
- **K-Means Algorithm**: The K-Means algorithm is applied in two different ways: with a library and without a library. The results are compared to analyze model performance.
- **PCA (Principal Component Analysis)**: PCA is used for dimensionality reduction before clustering.
- **Silhouette Score**: The Silhouette score is used to measure clustering performance.
- **Download Results**: The application allows downloading clustering results in `.csv` format.
- **Logging**: All operations and errors occurring in the application are logged.
- **Methods Served via Flask**: The application includes methods served via the Flask framework.
- **Unit Tests**: Unit tests have been developed for each method.

## K-Means Algorithm

### What is the K-Means Algorithm?

K-Means is one of the most popular clustering algorithms in unsupervised learning. This algorithm aims to group a dataset into a predefined number of clusters by associating each data point with its nearest cluster center. The primary goal of the algorithm is to partition the data into clusters.

### Steps of the K-Means Algorithm

1. **Determining the Number of Clusters (K value)**:  
    The K value, which is pre-determined by the user, defines the maximum number of clusters to be tested in the dataset.

2. **Random Selection of Initial Centroids**:  
    The algorithm randomly selects K centroids, located near the center of the data points, as starting points.

3. **Assigning Each Point to the Nearest Centroid**:  
    Each data point is associated with the nearest centroid and assigned to that centroid’s cluster. The distance metric used is typically the Euclidean distance.

4. **Updating Centroids**:  
    The new centroids are calculated by taking the average of all the data points in each cluster. This helps to better define the clusters.

5. **Reassigning and Updating**:  
    Data points are reassigned based on the updated centroids, and steps 3 and 4 are repeated until the cluster centroids no longer change.

6. **Termination of the Algorithm**:  
    The algorithm terminates when the cluster centroids remain stable.

### Example:
In a K-Means algorithm applied to a 2-dimensional dataset:
- Initially, 3 clusters are defined (K = 3).
- The algorithm groups the data points around 3 randomly selected centroids and iteratively updates these centroids to find the most optimal clusters.

### Example:
When applying the K-Means algorithm to a 2D dataset:
- Initially, 3 clusters (K = 3) are defined.
- The algorithm groups data points around 3 random centers and updates these centers in each iteration until the closest clusters are found.

### K-Means Without a Library
In this project, the K-Means algorithm is implemented from scratch without using any libraries. Each step of the algorithm is manually coded, and the data is clustered accordingly.

### K-Means with a Library
Alternatively, the `scikit-learn` library is used to provide a more optimized K-Means solution. `scikit-learn` is a popular Python library for quickly applying the K-Means algorithm and analyzing results.

### PCA (Principal Component Analysis)
Before running the clustering algorithm, PCA is used to reduce the dimensions of the data. PCA reduces high-dimensional data into two or three dimensions, making it more interpretable.

### What is the Silhouette Score?

The Silhouette Score is a metric that measures how well a clustering model performs. It is calculated for each data point as follows:

$$
\text{Silhouette Score} = \frac{b(i) - a(i)}{\max(a(i), b(i))}
$$

- **a(i)**: The average distance between the data point and other points in the same cluster.
- **b(i)**: The average distance between the data point and points in the nearest other cluster.

The Silhouette Score ranges between -1 and 1. Scores close to 1 indicate good clustering performance, scores close to 0 indicate that the data points are equally far from clusters, and negative scores suggest that points are clustered incorrectly.

## Logging

Operations and possible errors during the project are recorded using a logging system. This helps in tracking errors and producing solutions.

## Flask API

In this project, methods are served as an API using Flask. The application runs database operations, the K-Means algorithm, and logging functions via this API.

## Unit Tests

Unit tests have been developed for each method to ensure the application works as expected.

## Setup

To run the project in your local environment, follow these steps:

### Requirements
- Python
- PostgreSQL
- Flask
- React
- Docker (optional)

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/MFurkanYaman/KMeansWeb-Lib-vs-NoLib.git
    cd KMeansWeb-Lib-vs-NoLib
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```bash
    flask run
    ```

4. **Frontend (React) setup and run**:
    ```bash
    cd frontend
    npm install
    npm start
    ```
