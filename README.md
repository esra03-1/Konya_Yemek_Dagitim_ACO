# 🐜 Karınca Kolonisi Algoritması ile Yemek Dağıtım Optimizasyonu

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=flat&logo=streamlit)
![Folium](https://img.shields.io/badge/Folium-Maps-green?style=flat)
![Status](https://img.shields.io/badge/Durum-Tamamland%C4%B1-success)

Bu proje, **BLG-307 Yapay Zeka Sistemleri** dersi 2. Proje Ödevi kapsamında geliştirilmiştir. Konya ilindeki öğrenci yurtlarına yapılacak yemek dağıtımı için en kısa rotayı **Karınca Kolonisi Algoritması (ACO)** kullanarak optimize eder.

---

## 👤 Öğrenci Bilgileri

| **Bilgi** | **Detay** |
|-----------|-----------|
| **Adı Soyadı** | Esra Gögebakan |
| **Okul Numarası** | 2212721001 |
| **Bölüm** | Bilgisayar Mühendisliği |
| **Ders** | BLG-307 Yapay Zeka Sistemleri |

---

## 📌 Proje Tanımı (Senaryo 1)

> **Senaryo:** Konya ilinde sıcak yemek dağıtım hizmeti veren bir firmanın, merkez mutfaktan çıkarak **20 farklı öğrenci yurduna** yemek dağıtması gerekmektedir. Yemeğin soğumaması ve yakıt tasarrufu sağlanması amacıyla en kısa rotanın (Hamilton Döngüsü) bulunması hedeflenmiştir.

Bu problem, sürü zekası tabanlı **Karınca Kolonisi Optimizasyonu (ACO)** algoritması ile çözülmüş ve web arayüzüne aktarılmıştır.

---

## 🛠 Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|-----------|----------|
| **Python** 🐍 | Algoritma ve backend geliştirme dili. |
| **Streamlit** 👑 | Web tabanlı kullanıcı arayüzü (GUI). |
| **Folium** 🗺️ | Optimize edilen rotanın harita üzerinde çizimi. |
| **Google Maps API** 📍 | Gerçek yol mesafelerini (driving distance) hesaplamak için entegrasyon (Opsiyonel). |
| **Matplotlib** 📉 | Algoritmanın yakınsama (fitness) grafiğinin çizimi. |

---

## 📂 Dosya Yapısı

Proje klasör yapısı aşağıdaki gibidir:

```text
📁 aco_yemek_dagitim/
│
├── 📄 main.py             # Streamlit arayüzü ve ana uygulama
├── 📄 aco_algo.py         # Karınca Kolonisi Algoritması (Matematiksel Sınıf)
├── 📄 data_locations.py   # Konya yurtlarının gerçek koordinat verileri
├── 📄 requirements.txt    # Gerekli kütüphane listesi
└── 📄 README.md           # Proje dokümantasyonu
