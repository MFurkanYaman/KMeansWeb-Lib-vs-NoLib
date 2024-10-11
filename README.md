# KMeansWeb-Lib-vs-NoLib

Bu proje, Python kullanılarak geliştirilen bir web uygulamasıdır. Uygulama, K-Means algoritmasını hem kütüphane kullanarak hem de kütüphane kullanmadan çalıştırır. Sonuçlar, Silhouette Skoru ile kıyaslanarak en iyi küme sayısı belirlenir. Ayrıca, proje PostgreSQL kullanılarak veritabanına veri aktarımı, loglama, ve Flask ile metodların servis edilmesini içerir. Bu README dosyasında proje hakkında detaylı bilgi verilmektedir.

## Proje İçeriği

- **PostgreSQL**: Veriler, PostgreSQL veritabanına aktarılır ve uygulama bu verileri veritabanından tüketir.
- **K-Means Algoritması**: Kütüphane kullanarak ve kullanmadan iki farklı yöntemle K-Means algoritması uygulanmıştır. Sonuçlar karşılaştırılarak model performansı analiz edilmiştir.
- **PCA (Principal Component Analysis)**: Kümeleme işlemi öncesinde boyut indirgeme işlemi olarak PCA kullanılmıştır.
- **Silhouette Skoru**: Kümeleme performansını ölçmek için Silhouette skoru kullanılmıştır.
- **Sonuçları İndirme**: Uygulama, kümeleme işleminin sonuçlarını `.csv` formatında indirmenize olanak tanır.
- **Loglama**: Uygulama içerisinde meydana gelen işlemler ve hatalar loglanarak kaydedilmiştir.
- **Flask ile Servis Edilen Metodlar**: Uygulama, Flask framework'ü kullanarak servis edilen metodlar içerir.
- **Unit Testler**: Her bir metod için birim testler geliştirilmiştir.
  
## Video Tanıtımı

Projenin çalışma mantığını gösteren bir video hazırladım. Videoyu izlemek için [buraya tıklayın](#). Video, uygulamanın nasıl çalıştığını ve ana özelliklerini detaylı bir şekilde açıklamaktadır.

## K-Means Algoritması

### K-Means Algoritması Nedir?

K-Means, denetimsiz öğrenme yöntemlerinden biri olan kümeleme algoritmaları arasında en popüler olanıdır. Bu algoritma, bir veri setini belirli sayıda kümeye ayırarak, her bir kümeye en yakın veri noktalarını gruplamayı amaçlar. Algoritmanın temel amacı, verileri kümelere ayırmak ve her bir kümenin merkezi bir noktasını (centroid) belirlemektir.

### K-Means Algoritmasının Çalışma Adımları

1. **Kümelerin Sayısının Belirlenmesi (K değeri)**:
    Kullanıcı tarafından önceden belirlenen K değeri, veri setindeki kaç küme oluşacağını belirler.

2. **Başlangıç Merkezlerinin Rastgele Seçilmesi**:
    Algoritma, verilerin merkezine yakın rastgele K adet merkezi başlangıç noktası olarak seçer.

3. **Her Noktanın En Yakın Merkeze Atanması**:
    Her bir veri noktası, en yakın olduğu merkez ile ilişkilendirilir ve o merkezin kümesine dahil edilir. Mesafe ölçütü olarak genellikle Öklid (Euclidean) mesafesi kullanılır.

4. **Merkezlerin Güncellenmesi**:
    Her bir kümedeki veri noktalarının ortalaması alınarak, yeni kümelerin merkezleri hesaplanır. Bu işlem, kümelerin daha iyi tanımlanmasına yardımcı olur.

5. **Tekrar Atama ve Güncelleme**:
    Veri noktaları, yeni merkezlere göre tekrar atanır ve adımlar 3 ve 4, küme merkezleri artık değişmeyene kadar tekrarlanır.

6. **Algoritmanın Sonlanması**:
    Küme merkezleri sabit kaldığında veya belirlenen maksimum iterasyon sayısına ulaşıldığında, algoritma sonlanır.

### Örnek:
Bir K-Means algoritması uygulandığında, 2 boyutlu bir veri seti şu şekilde çalışır:
- Başlangıçta 3 küme (K = 3) belirlenmiştir.
- Algoritma, veri noktalarını 3 rastgele merkez etrafında gruplar ve her iterasyonda bu merkezleri güncelleyerek en yakın kümeyi bulur.

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

