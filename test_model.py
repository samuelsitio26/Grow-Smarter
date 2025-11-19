import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load('model_cluster.pkl')
scaler = joblib.load('scaler.pkl')
cluster_info = joblib.load('cluster_info.pkl')

print("="*60)
print("INFORMASI MODEL")
print("="*60)
print(f"Jumlah Cluster: {len(cluster_info)}")
print(f"\nCharacteristics setiap cluster:")
print(cluster_info)

print("\n" + "="*60)
print("TEST PREDIKSI DENGAN BERBAGAI INPUT")
print("="*60)

# Test dengan berbagai input
test_cases = [
    {"N": 10, "P": 100, "K": 50, "temperature": 30, "humidity": 60, "ph": 6, "rainfall": 200, "desc": "N Rendah"},
    {"N": 150, "P": 20, "K": 50, "temperature": 30, "humidity": 60, "ph": 6, "rainfall": 200, "desc": "N Tinggi"},
    {"N": 75, "P": 55, "K": 56, "temperature": 27, "humidity": 60, "ph": 6.5, "rainfall": 200, "desc": "Mirip Cluster 0"},
    {"N": 125, "P": 55, "K": 54, "temperature": 28, "humidity": 60, "ph": 6.5, "rainfall": 198, "desc": "Mirip Cluster 1"},
    {"N": 50, "P": 30, "K": 40, "temperature": 20, "humidity": 80, "ph": 5, "rainfall": 150, "desc": "Semua Rendah"},
    {"N": 140, "P": 80, "K": 80, "temperature": 40, "humidity": 40, "ph": 7, "rainfall": 250, "desc": "Semua Tinggi"},
]

features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

for i, test in enumerate(test_cases, 1):
    desc = test.pop('desc')
    df = pd.DataFrame([test], columns=features)
    df_scaled = scaler.transform(df)
    pred = model.predict(df_scaled)[0]
    
    # Hitung jarak ke setiap cluster center
    distances = []
    for j, center in enumerate(model.cluster_centers_):
        dist = np.linalg.norm(df_scaled[0] - center)
        distances.append((j, dist))
    
    print(f"\nTest {i}: {desc}")
    print(f"  Input: N={test['N']}, P={test['P']}, K={test['K']}, T={test['temperature']}")
    print(f"  Predicted Cluster: {pred}")
    print(f"  Jarak ke Cluster 0: {distances[0][1]:.4f}")
    print(f"  Jarak ke Cluster 1: {distances[1][1]:.4f}")

print("\n" + "="*60)
print("KESIMPULAN")
print("="*60)
print("Jika semua prediksi menunjukkan cluster yang sama,")
print("kemungkinan ada masalah dengan model atau data training.")
