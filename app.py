from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load model clustering dan scaler
try:
    model_cluster = joblib.load("model_cluster.pkl")
    scaler = joblib.load("scaler.pkl")
    cluster_info = joblib.load("cluster_info.pkl")
except Exception as e:
    print(f"[ERROR] Gagal memuat file: {e}")
    print("[INFO] Pastikan sudah menjalankan train_model.py terlebih dahulu")
    exit()

# Route halaman utama
@app.route('/')
def index():
     return render_template('index.html')

@app.route('/input')
def input_data():
    return render_template('input_data.html')

# Route prediksi cluster
@app.route('/predict', methods=["POST"])
def predict():
    data = request.get_json()
    
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    try:
        # Buat dataframe input dan scaling
        df_input = pd.DataFrame([data], columns=features)
        df_scaled = scaler.transform(df_input)

        # Prediksi cluster
        cluster_pred = model_cluster.predict(df_scaled)[0]
        
        # Hitung jarak ke cluster center
        cluster_center = model_cluster.cluster_centers_[cluster_pred]
        distance_to_center = np.linalg.norm(df_scaled[0] - cluster_center)
        
        # Ambil karakteristik cluster
        cluster_characteristics = cluster_info.iloc[cluster_pred].to_dict()
        
        # Hitung fertility score (formula sederhana)
        fertility_score = data['N'] * 0.4 + data['P'] * 0.3 + data['K'] * 0.3
        fertility_score = round(fertility_score, 2)
        
        # Deskripsi cluster berdasarkan karakteristik
        cluster_desc = generate_cluster_description(cluster_pred, cluster_characteristics)

        return jsonify({
            "cluster": int(cluster_pred),
            "cluster_name": f"Cluster {cluster_pred}",
            "distance_to_center": round(float(distance_to_center), 4),
            "fertility_score": fertility_score,
            "cluster_characteristics": cluster_characteristics,
            "cluster_description": cluster_desc
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

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

if __name__ == "__main__":
    app.run(debug=True)