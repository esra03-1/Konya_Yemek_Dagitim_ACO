\# Karınca Kolonisi Algoritması ile Yemek Dağıtım Optimizasyonu (ACO)



Bu proje, \*\*BLG-307 Yapay Zeka Sistemleri\*\* dersi 2. Proje Ödevi kapsamında hazırlanmıştır.



\## 👤 Öğrenci Bilgileri

\* \*\*Adı Soyadı:\*\* Esra Gögebakan

\* \*\*Okul Numarası:\*\* 2212721001

\* \*\*Bölüm:\*\* Bilgisayar Mühendisliği



\## 📌 Proje Tanımı

\*\*Senaryo 1:\*\* Konya ilinde sıcak yemek dağıtım hizmeti veren bir firmanın, merkez mutfaktan çıkarak \*\*20 farklı öğrenci yurduna\*\* yemek dağıtması gerekmektedir. Yemeğin soğumaması ve yakıt tasarrufu sağlanması amacıyla en kısa rotanın (Hamilton Döngüsü) bulunması hedeflenmiştir.



Bu problem, \*\*Karınca Kolonisi Optimizasyonu (Ant Colony Optimization - ACO)\*\* algoritması kullanılarak çözülmüştür.



\## 🛠 Kullanılan Teknolojiler ve Yöntemler

\* \*\*Python:\*\* Projenin ana programlama dili.

\* \*\*Streamlit:\*\* Web tabanlı kullanıcı arayüzü (GUI) oluşturmak için kullanıldı.

\* \*\*Folium:\*\* Optimize edilen rotanın harita üzerinde görselleştirilmesi için kullanıldı.

\* \*\*Google Maps API (Opsiyonel):\*\* Gerçek yol mesafelerini (driving distance) hesaplamak için entegre edildi. API anahtarı girilmezse veya kota aşılırsa \*\*Haversine Formülü\*\* (Kuş uçuşu mesafe) devreye girer.

\* \*\*Matplotlib:\*\* Algoritmanın yakınsama (convergence) grafiğini çizdirmek için kullanıldı.



\## 📂 Dosya Yapısı

\* `main.py`: Uygulamanın ana giriş noktasıdır. Streamlit arayüzü, harita çizimi ve kullanıcı parametreleri burada yönetilir.

\* `aco\_algo.py`: Karınca Kolonisi Algoritması'nın matematiksel sınıfını içerir (Feromon güncelleme, olasılık hesaplama, rulet tekerleği seçimi).

\* `data\_locations.py`: Konya'daki merkez mutfak ve 19 öğrenci yurdunun gerçek koordinat verilerini içerir.

\* `requirements.txt`: Projenin çalışması için gerekli kütüphanelerin listesidir.



\## 🚀 Kurulum ve Çalıştırma



Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:



1\. \*\*Gerekli Kütüphaneleri Yükleyin:\*\*

&nbsp;  Terminali proje klasöründe açın ve şu komutu yazın:

&nbsp;  ```bash

&nbsp;  pip install -r requirements.txt

