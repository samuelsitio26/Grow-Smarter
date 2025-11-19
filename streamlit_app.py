import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Page configuration
st.set_page_config(
    page_title="SoilSense - Clustering System",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2d6a4f;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #52796f;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f1faee;
        border-left: 5px solid #2d6a4f;
        margin: 1rem 0;
        color: #1a1a1a;
    }
    .result-box h3 {
        color: #2d6a4f;
    }
    .result-box p {
        color: #333333;
    }
    .metric-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #e8f5e9;
        text-align: center;
        margin: 0.5rem 0;
        color: #1a1a1a;
    }
    .metric-box h3, .metric-box h2, .metric-box p {
        color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Load models
@st.cache_resource
def load_models():
    try:
        model_cluster = joblib.load("model_cluster.pkl")
        scaler = joblib.load("scaler.pkl")
        cluster_info = joblib.load("cluster_info.pkl")
        return model_cluster, scaler, cluster_info
    except Exception as e:
        st.error(f"❌ Error loading model files: {e}")
        st.info("💡 Make sure you have run `train_model.py` first to generate the model files.")
        st.stop()

model_cluster, scaler, cluster_info = load_models()

def generate_cluster_description(cluster_id, characteristics):
    """Generate description based on cluster characteristics"""
    desc_parts = []
    
    # Analisis berdasarkan nilai fitur
    if characteristics['N'] > 100:
        desc_parts.append("tinggi nitrogen")
    elif characteristics['N'] < 70:
        desc_parts.append("rendah nitrogen")
    else:
        desc_parts.append("sedang nitrogen")
    
    if characteristics['P'] > 60:
        desc_parts.append("tinggi fosfor")
    elif characteristics['P'] < 40:
        desc_parts.append("rendah fosfor")
    
    if characteristics['K'] > 60:
        desc_parts.append("tinggi kalium")
    elif characteristics['K'] < 40:
        desc_parts.append("rendah kalium")
    
    if characteristics['temperature'] > 30:
        desc_parts.append("suhu tinggi")
    elif characteristics['temperature'] < 20:
        desc_parts.append("suhu rendah")
    
    if characteristics['rainfall'] > 200:
        desc_parts.append("curah hujan tinggi")
    elif characteristics['rainfall'] < 150:
        desc_parts.append("curah hujan rendah")
    
    description = f"Cluster {cluster_id} memiliki karakteristik tanah dengan kandungan " + ", ".join(desc_parts) + "."
    return description

def get_fertility_category(score):
    """Categorize fertility score"""
    if score < 26:
        return "Very Low", "🔴"
    elif score < 60:
        return "Low", "🟠"
    elif score < 90:
        return "Moderate", "🟡"
    elif score < 120:
        return "High", "🟢"
    else:
        return "Very High", "🔵"

# Header
st.markdown('<div class="main-header">🌱 SoilSense</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Clustering System - Unsupervised Learning untuk Analisis Kondisi Tanah</div>', unsafe_allow_html=True)

# Sidebar - Info
with st.sidebar:
    st.header("📖 Tentang Aplikasi")
    st.write("""
    **SoilSense** menggunakan **K-Means Clustering** (Unsupervised Learning) 
    untuk mengelompokkan kondisi tanah berdasarkan karakteristiknya.
    """)
    
    st.header("📊 Parameter Input")
    st.info("""
    **Nitrogen (N):** 50-150  
    **Phosphorus (P):** 10-100  
    **Potassium (K):** 10-100  
    **Temperature:** 15-48°C  
    **Humidity:** 20-100%  
    **pH:** 4-8  
    **Rainfall:** 100-300mm
    """)
    
    st.header("🎯 Cara Kerja")
    st.write("""
    1. Input data kondisi tanah
    2. Model clustering memprediksi kelompok
    3. Sistem menampilkan karakteristik cluster
    4. Menghitung fertility score
    """)

# Main content
st.header("📝 Input Data Kondisi Tanah")

col1, col2 = st.columns(2)

with col1:
    nitrogen = st.number_input(
        "🔵 Nitrogen (N)", 
        min_value=0, 
        max_value=200, 
        value=80,
        help="Kandungan nitrogen dalam tanah (50-150)"
    )
    
    phosphorus = st.number_input(
        "🟣 Phosphorus (P)", 
        min_value=0, 
        max_value=150, 
        value=50,
        help="Kandungan fosfor dalam tanah (10-100)"
    )
    
    potassium = st.number_input(
        "🟢 Potassium (K)", 
        min_value=0, 
        max_value=150, 
        value=50,
        help="Kandungan kalium dalam tanah (10-100)"
    )
    
    temperature = st.number_input(
        "🌡️ Temperature (°C)", 
        min_value=0.0, 
        max_value=60.0, 
        value=25.0,
        step=0.1,
        help="Suhu lingkungan (15-48°C)"
    )

with col2:
    humidity = st.number_input(
        "💧 Humidity (%)", 
        min_value=0.0, 
        max_value=100.0, 
        value=65.0,
        step=0.1,
        help="Kelembaban udara (20-100%)"
    )
    
    ph = st.number_input(
        "⚗️ pH", 
        min_value=0.0, 
        max_value=14.0, 
        value=6.5,
        step=0.1,
        help="Tingkat keasaman tanah (4-8)"
    )
    
    rainfall = st.number_input(
        "🌧️ Rainfall (mm)", 
        min_value=0.0, 
        max_value=500.0, 
        value=150.0,
        step=0.1,
        help="Curah hujan (100-300mm)"
    )

st.markdown("---")

# Predict button
if st.button("🔍 Get Prediction", type="primary", use_container_width=True):
    
    # Prepare input data
    input_data = {
        'N': nitrogen,
        'P': phosphorus,
        'K': potassium,
        'temperature': temperature,
        'humidity': humidity,
        'ph': ph,
        'rainfall': rainfall
    }
    
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    df_input = pd.DataFrame([input_data], columns=features)
    
    # Scale input
    df_scaled = scaler.transform(df_input)
    
    # Predict cluster
    cluster_pred = model_cluster.predict(df_scaled)[0]
    
    # Calculate distance to cluster center
    cluster_center = model_cluster.cluster_centers_[cluster_pred]
    distance_to_center = np.linalg.norm(df_scaled[0] - cluster_center)
    
    # Get cluster characteristics
    cluster_characteristics = cluster_info.iloc[cluster_pred].to_dict()
    
    # Calculate fertility score
    fertility_score = nitrogen * 0.4 + phosphorus * 0.3 + potassium * 0.3
    fertility_category, fertility_icon = get_fertility_category(fertility_score)
    
    # Generate description
    cluster_desc = generate_cluster_description(cluster_pred, cluster_characteristics)
    
    # Display results
    st.success("✅ Prediksi berhasil!")
    
    st.header("📊 Hasil Prediksi")
    
    # Metrics row
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>🏷️ Cluster</h3>
            <h2>Cluster {cluster_pred}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3>{fertility_icon} Fertility Score</h3>
            <h2>{fertility_score:.2f}</h2>
            <p><strong>{fertility_category}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
        <div class="metric-box">
            <h3>📍 Distance to Center</h3>
            <h2>{distance_to_center:.4f}</h2>
            <p>Similarity measure</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Description
    st.markdown(f"""
    <div class="result-box">
        <h3>📝 Deskripsi Cluster</h3>
        <p style="font-size: 1.1rem; line-height: 1.6;">{cluster_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cluster characteristics
    st.subheader("📈 Karakteristik Cluster (Rata-rata)")
    
    char_col1, char_col2 = st.columns(2)
    
    with char_col1:
        st.metric("🔵 Nitrogen (N)", f"{cluster_characteristics['N']:.2f}")
        st.metric("🟣 Phosphorus (P)", f"{cluster_characteristics['P']:.2f}")
        st.metric("🟢 Potassium (K)", f"{cluster_characteristics['K']:.2f}")
        st.metric("🌡️ Temperature", f"{cluster_characteristics['temperature']:.2f} °C")
    
    with char_col2:
        st.metric("💧 Humidity", f"{cluster_characteristics['humidity']:.2f} %")
        st.metric("⚗️ pH", f"{cluster_characteristics['ph']:.2f}")
        st.metric("🌧️ Rainfall", f"{cluster_characteristics['rainfall']:.2f} mm")
    
    # Additional info
    with st.expander("ℹ️ Penjelasan Hasil"):
        st.write("""
        **Cluster Number**: Nomor kelompok kondisi tanah yang memiliki karakteristik serupa.
        
        **Fertility Score**: Dihitung berdasarkan formula: `N × 0.4 + P × 0.3 + K × 0.3`
        - Menunjukkan tingkat kesuburan tanah berdasarkan kandungan NPK
        
        **Distance to Center**: Jarak dari input Anda ke pusat cluster
        - Semakin kecil = semakin mirip dengan karakteristik cluster
        
        **Cluster Characteristics**: Nilai rata-rata dari semua data dalam cluster
        - Menunjukkan profil umum kondisi tanah dalam kelompok ini
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #52796f; padding: 1rem;">
    <p><strong>🌱 SoilSense - Clustering System</strong></p>
    <p>Powered by K-Means Clustering (Unsupervised Learning) | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
