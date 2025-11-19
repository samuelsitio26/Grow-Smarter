# Alasan Project Ini Menggunakan Unsupervised Learning

## 📋 Ringkasan

Project **SoilSense** menggunakan **Unsupervised Learning (K-Means Clustering)** untuk mengelompokkan kondisi tanah berdasarkan karakteristiknya. Berikut adalah alasan-alasan mengapa project ini dikategorikan sebagai unsupervised learning.

---

## ✅ Alasan Utama: Project Ini Adalah Unsupervised Learning

### 1. **Tidak Menggunakan Label Data untuk Training**

**Bukti di Kode:**
```python
# train_model.py - Line 67-68
# Persiapan data untuk unsupervised learning
X = df[features]  # Hanya menggunakan fitur, TIDAK menggunakan kolom 'label'
```

**Penjelasan:**
- Dataset `data_core.csv` memiliki kolom `label` yang berisi nama tanaman (Wheat, Rice, Millet, dll)
- **NAMUN**, kolom `label` ini **TIDAK DIGUNAKAN** sama sekali dalam proses training
- Model hanya belajar dari fitur: `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`
- Model menemukan pola sendiri tanpa tahu "tanaman apa yang cocok"

**Perbandingan:**
- ❌ **Supervised Learning**: Akan menggunakan `X` (fitur) + `y` (label) untuk training
- ✅ **Unsupervised Learning (Project Ini)**: Hanya menggunakan `X` (fitur) saja

---

### 2. **Output Adalah Cluster Assignment, Bukan Prediksi Label**

**Bukti di Kode:**
```python
# app.py - Line 39-40
cluster_pred = model_cluster.predict(df_scaled)[0]  # Output: angka (0, 1, 2, ...)

# app.py - Line 56-63
return jsonify({
    "cluster": int(cluster_pred),  # Bukan "Wheat" atau "Rice"
    "cluster_name": f"Cluster {cluster_pred}",
    "cluster_characteristics": cluster_characteristics,
    "cluster_description": cluster_desc
})
```

**Penjelasan:**
- Output model adalah **nomor cluster** (0, 1, 2, 3, ...), bukan nama tanaman
- Sistem menampilkan **karakteristik cluster**, bukan prediksi "tanaman apa yang cocok"
- Tidak ada mapping dari cluster ke label tanaman

**Perbandingan:**
- ❌ **Supervised Learning**: Output = "Wheat", "Rice", "Millet" (nama tanaman)
- ✅ **Unsupervised Learning (Project Ini)**: Output = 0, 1, 2, 3 (nomor cluster)

---

### 3. **Menggunakan Algoritma Unsupervised Learning**

**Bukti di Kode:**
```python
# train_model.py - Line 7
from sklearn.cluster import KMeans  # Algoritma unsupervised learning

# train_model.py - Line 84-87
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(X_scaled)  # Hanya butuh X, tidak butuh y (label)
```

**Penjelasan:**
- **K-Means Clustering** adalah algoritma **unsupervised learning** yang terkenal
- K-Means bekerja dengan cara:
  1. Memilih K titik acak sebagai centroid
  2. Mengelompokkan data berdasarkan jarak ke centroid terdekat
  3. Update centroid berdasarkan rata-rata data dalam cluster
  4. Iterasi sampai konvergen
- **Tidak membutuhkan label** untuk belajar

**Perbandingan:**
- ❌ **Supervised Learning**: Decision Tree, Random Forest, SVM (butuh label)
- ✅ **Unsupervised Learning (Project Ini)**: K-Means Clustering (tidak butuh label)

---

### 4. **Evaluasi Menggunakan Metrik Clustering, Bukan Classification Metrics**

**Bukti di Kode:**
```python
# train_model.py - Line 8
from sklearn.metrics import silhouette_score, davies_bouldin_score

# train_model.py - Line 119-123
silhouette_avg = silhouette_score(X_scaled, cluster_labels)
davies_bouldin = davies_bouldin_score(X_scaled, cluster_labels)
print(f"[INFO] Silhouette Score: {silhouette_avg:.4f}")
print(f"[INFO] Davies-Bouldin Score: {davies_bouldin:.4f}")
```

**Penjelasan:**
- **Silhouette Score**: Mengukur seberapa baik data point cocok dengan cluster-nya (range: -1 sampai 1)
- **Davies-Bouldin Score**: Mengukur rasio jarak intra-cluster dan inter-cluster
- **TIDAK menggunakan** accuracy, precision, recall, confusion matrix (metrik supervised learning)

**Perbandingan:**
- ❌ **Supervised Learning**: Accuracy, Precision, Recall, F1-Score, Confusion Matrix
- ✅ **Unsupervised Learning (Project Ini)**: Silhouette Score, Davies-Bouldin Score

---

### 5. **Tujuan: Menemukan Pola, Bukan Memprediksi Label**

**Penjelasan:**
- **Tujuan Unsupervised Learning**: Menemukan struktur tersembunyi dalam data tanpa tahu "jawaban yang benar"
- **Tujuan Project Ini**: Mengelompokkan kondisi tanah yang serupa, bukan memprediksi "tanaman apa yang cocok"
- Model menemukan pola sendiri: "Kondisi tanah dengan N tinggi, P sedang, K rendah cenderung berada dalam cluster yang sama"

**Perbandingan:**
- ❌ **Supervised Learning**: "Dengan kondisi ini, tanaman yang cocok adalah Wheat"
- ✅ **Unsupervised Learning (Project Ini)**: "Kondisi ini termasuk dalam Cluster 2, yang memiliki karakteristik tinggi nitrogen, sedang fosfor, rendah kalium"

---

## 🔍 Bukti Tambahan dari Kode

### Bukti 1: Tidak Ada LabelEncoder untuk Label Tanaman

**Jika Supervised Learning:**
```python
# Akan ada kode seperti ini (TIDAK ADA di project ini):
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(df['label'])  # Encode label tanaman
```

**Di Project Ini:**
- ❌ Tidak ada `LabelEncoder` untuk kolom `label`
- ✅ Hanya ada `StandardScaler` untuk fitur numerik

---

### Bukti 2: Tidak Ada Train-Test Split dengan Stratify

**Jika Supervised Learning:**
```python
# Akan ada kode seperti ini (TIDAK ADA di project ini):
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y  # Stratify berdasarkan label
)
```

**Di Project Ini:**
- ❌ Tidak ada train-test split
- ✅ Semua data digunakan untuk clustering (karena tidak ada label untuk diuji)

---

### Bukti 3: Tidak Ada Classification Report atau Confusion Matrix

**Jika Supervised Learning:**
```python
# Akan ada kode seperti ini (TIDAK ADA di project ini):
from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
```

**Di Project Ini:**
- ❌ Tidak ada classification report
- ❌ Tidak ada confusion matrix
- ✅ Hanya ada evaluasi clustering (Silhouette Score, Davies-Bouldin)

---

## 📊 Perbandingan Lengkap: Supervised vs Unsupervised

| Aspek | Supervised Learning | Project Ini (Unsupervised) |
|-------|---------------------|---------------------------|
| **Data Training** | Fitur + Label | Hanya Fitur |
| **Kolom 'label' digunakan?** | ✅ Ya (untuk training) | ❌ Tidak (diabaikan) |
| **Algoritma** | Decision Tree, SVM, dll | K-Means Clustering |
| **Output** | Nama tanaman (Wheat, Rice) | Nomor cluster (0, 1, 2) |
| **Evaluasi** | Accuracy, Precision, Recall | Silhouette Score, Davies-Bouldin |
| **Tujuan** | Prediksi label baru | Menemukan pola/kelompok |
| **LabelEncoder** | ✅ Ada | ❌ Tidak ada |
| **Train-Test Split** | ✅ Ada (dengan stratify) | ❌ Tidak ada |
| **Classification Report** | ✅ Ada | ❌ Tidak ada |

---

## 🎯 Kesimpulan

Project **SoilSense** adalah **Unsupervised Learning** karena:

1. ✅ **Tidak menggunakan label** untuk training (kolom 'label' diabaikan)
2. ✅ **Output adalah cluster assignment**, bukan prediksi label tanaman
3. ✅ **Menggunakan K-Means Clustering**, algoritma unsupervised learning
4. ✅ **Evaluasi menggunakan metrik clustering**, bukan classification metrics
5. ✅ **Tujuan menemukan pola**, bukan memprediksi label
6. ✅ **Tidak ada komponen supervised learning** (LabelEncoder, train-test split, classification report)

**Catatan Penting:**
- Adanya **input form** dan **clustering result** adalah **NORMAL** dalam unsupervised learning
- Input form digunakan untuk memasukkan data baru yang akan di-cluster
- Clustering result menampilkan hasil pengelompokan (cluster assignment)
- Ini berbeda dengan supervised learning yang memprediksi label (nama tanaman)

---

## 📝 Referensi Kode

### File-file Penting:

1. **train_model.py**:
   - Line 67-68: Hanya menggunakan fitur, tidak menggunakan label
   - Line 84-87: Training K-Means (unsupervised algorithm)
   - Line 119-123: Evaluasi dengan metrik clustering

2. **app.py**:
   - Line 39-40: Predict cluster (bukan label)
   - Line 56-63: Return cluster assignment (bukan nama tanaman)

3. **data_core.csv**:
   - Memiliki kolom 'label' tapi **TIDAK DIGUNAKAN** dalam training

---

**Dibuat untuk menjelaskan mengapa SoilSense menggunakan Unsupervised Learning** 🌱

