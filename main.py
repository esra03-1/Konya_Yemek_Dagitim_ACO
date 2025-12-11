# main.py
import streamlit as st
import numpy as np
import pandas as pd
import googlemaps
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium

# Kendi modüllerimiz
from data_locations import KONYA_LOKASYONLARI
from aco_algo import AntColonyOptimizer

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Konya Yemek Dağıtım Optimizasyonu", layout="wide")

# --- SESSION STATE BAŞLATMA (HAFIZA) ---
# Sonuçların kaybolmaması için hafıza değişkenleri oluşturuyoruz
if 'run_completed' not in st.session_state:
    st.session_state.run_completed = False
if 'best_path' not in st.session_state:
    st.session_state.best_path = None
if 'best_dist' not in st.session_state:
    st.session_state.best_dist = 0
if 'history' not in st.session_state:
    st.session_state.history = []

# --- YARDIMCI FONKSİYONLAR ---

def haversine_distance(lat1, lon1, lat2, lon2):
    """API Key yoksa veya kota aşılırsa kuş uçuşu mesafe hesaplar"""
    R = 6371000 # Dünya yarıçapı (metre)
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2) * sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

def get_distance_matrix(locations, api_key=None):
    """
    Google Maps API kullanarak veya Haversine formülü ile mesafe matrisi oluşturur.
    """
    n = len(locations)
    matrix = np.zeros((n, n))
    
    # API Key varsa Google Maps servisini dene
    gmaps = None
    if api_key:
        try:
            gmaps = googlemaps.Client(key=api_key)
        except Exception as e:
            st.error(f"API Hatası: {e}")
    
    # İlerleme çubuğu
    progress_bar = st.progress(0)
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0
            else:
                dist = 0
                # DEMO MODU: API Key girilse bile kota dostu olması için Haversine kullanıyoruz.
                # Gerçek veri için aşağıdaki False'u True yapabilirsiniz (Dikkat: Kota yer).
                if False and gmaps: 
                    try:
                        result = gmaps.distance_matrix(
                            origins=(locations[i]['lat'], locations[i]['lon']),
                            destinations=(locations[j]['lat'], locations[j]['lon']),
                            mode="driving"
                        )
                        dist = result['rows'][0]['elements'][0]['distance']['value']
                    except:
                        dist = haversine_distance(
                            locations[i]['lat'], locations[i]['lon'],
                            locations[j]['lat'], locations[j]['lon']
                        )
                else:
                    dist = haversine_distance(
                        locations[i]['lat'], locations[i]['lon'],
                        locations[j]['lat'], locations[j]['lon']
                    )
                
                matrix[i][j] = dist
        
        progress_bar.progress((i + 1) / n)
    
    progress_bar.empty()
    return matrix

# --- ARAYÜZ ---

st.title("🐜 ACO ile Konya Yemek Dağıtım Rotası Optimizasyonu")
st.markdown("""
**Senaryo 1:** Konya'daki yemek firmasından 20 öğrenci yurduna en kısa sürede dağıtım yapılması.
**Algoritma:** Karınca Kolonisi Optimizasyonu (ACO)
""")

# Yan Menü - Ayarlar
with st.sidebar:
    st.header("⚙️ Parametreler")
    
    default_api_key = ""
    try:
        if "general" in st.secrets and "google_api_key" in st.secrets["general"]:
            default_api_key = st.secrets["general"]["google_api_key"]
            st.success("API Anahtarı yüklendi! ✅")
    except:
        pass

    api_key = st.text_input("Google Maps API Key", value=default_api_key, type="password")
    
    st.divider()
    n_ants = st.slider("Karınca Sayısı", 5, 50, 20)
    n_iterations = st.slider("İterasyon Sayısı", 10, 200, 50)
    alpha = st.slider("Alpha (Feromon Etkisi)", 0.1, 5.0, 1.0)
    beta = st.slider("Beta (Mesafe Etkisi)", 0.1, 5.0, 2.0)
    evaporation = st.slider("Buharlaşma Oranı", 0.0, 1.0, 0.5)
    
    # Butona basılınca işlemi başlat ama çizimi aşağıda yap
    if st.button("Rotayı Optimize Et"):
        with st.spinner('Mesafe matrisi hesaplanıyor ve en kısa yol aranıyor...'):
            # 1. Mesafe Matrisini Oluştur
            dist_matrix = get_distance_matrix(KONYA_LOKASYONLARI, api_key)
            
            # 2. Algoritmayı Çalıştır
            optimizer = AntColonyOptimizer(
                distance_matrix=dist_matrix,
                n_ants=n_ants,
                n_iterations=n_iterations,
                alpha=alpha,
                beta=beta,
                evaporation_rate=evaporation,
                Q=100000 
            )
            
            best_path, best_dist, history = optimizer.run()
            
            # 3. Sonuçları Hafızaya (Session State) Kaydet
            st.session_state.run_completed = True
            st.session_state.best_path = best_path
            st.session_state.best_dist = best_dist
            st.session_state.history = history

# Ana Ekran Düzeni
col1, col2 = st.columns([2, 1])

# --- SONUÇLARI GÖSTERME KISMI (Hafızadan Okur) ---
if st.session_state.run_completed:
    # Hafızadaki verileri al
    best_path = st.session_state.best_path
    best_dist = st.session_state.best_dist
    history = st.session_state.history
    
    st.success(f"✅ Optimizasyon Tamamlandı! Toplam Mesafe: {best_dist/1000:.2f} km")
    
    # --- GRAFİK ---
    fig, ax = plt.subplots()
    ax.plot(history, color='green', linewidth=2)
    ax.set_title("Yakınsama Grafiği (Mesafe Değişimi)")
    ax.set_xlabel("İterasyon")
    ax.set_ylabel("Toplam Mesafe (m)")
    ax.grid(True, linestyle='--', alpha=0.7)
    col2.pyplot(fig)
    
    # --- HARİTA ---
    start_lat = KONYA_LOKASYONLARI[0]['lat']
    start_lon = KONYA_LOKASYONLARI[0]['lon']
    m = folium.Map(location=[start_lat, start_lon], zoom_start=13)
    
    points = []
    
    # Rota üzerindeki noktaları sırasıyla işaretle
    for sira_no, idx in enumerate(best_path):
        loc = KONYA_LOKASYONLARI[idx]
        points.append([loc['lat'], loc['lon']])
        
        # Renk ve İkon Ayarları
        if idx == 0:
            icon_color = 'red'
            icon_type = 'home'
            popup_text = f"BAŞLANGIÇ/BİTİŞ: {loc['name']}"
        else:
            icon_color = 'blue'
            icon_type = 'info-sign'
            popup_text = f"{sira_no}. Sırada: {loc['name']}"
        
        folium.Marker(
            [loc['lat'], loc['lon']],
            popup=popup_text,
            tooltip=f"{sira_no}. {loc['name']}",
            icon=folium.Icon(color=icon_color, icon=icon_type)
        ).add_to(m)
        
    # Çizgiyi ekle (Rota)
    folium.PolyLine(points, color="red", weight=4, opacity=0.7).add_to(m)
    
    with col1:
        st_folium(m, width=700, height=500)
    
    # --- DETAYLI LİSTE ---
    st.subheader("📍 Adım Adım Dağıtım Rotası")
    st.markdown("Aşağıdaki liste, karınca kolonisi algoritmasının belirlediği **en verimli** dağıtım sırasıdır:")
    
    liste_col1, liste_col2 = st.columns(2)
    
    rota_adimlari = []
    for i, idx in enumerate(best_path):
        isim = KONYA_LOKASYONLARI[idx]['name']
        if i == 0:
            rota_adimlari.append(f"🏁 **BAŞLANGIÇ:** {isim}")
        elif i == len(best_path) - 1:
            rota_adimlari.append(f"🏁 **BİTİŞ:** {isim}")
        else:
            rota_adimlari.append(f"**{i}.** {isim}")
    
    half = len(rota_adimlari) // 2
    with liste_col1:
        for adim in rota_adimlari[:half+1]:
            st.write(adim)
    with liste_col2:
        for adim in rota_adimlari[half+1:]:
            st.write(adim)

else:
    # Henüz çalıştırılmadıysa boş harita göster
    st.info("Ayarları kontrol edip 'Rotayı Optimize Et' butonuna basınız.")
    
    start_lat = KONYA_LOKASYONLARI[0]['lat']
    start_lon = KONYA_LOKASYONLARI[0]['lon']
    m_start = folium.Map(location=[start_lat, start_lon], zoom_start=12)
    
    for loc in KONYA_LOKASYONLARI:
        icon_color = 'red' if loc['id'] == 0 else 'gray'
        folium.Marker(
            [loc['lat'], loc['lon']], 
            popup=loc['name'],
            icon=folium.Icon(color=icon_color)
        ).add_to(m_start)
    
    with col1:
        st_folium(m_start, width=700, height=500)