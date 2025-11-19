# SoilSense - Clustering System 🌱

**SoilSense** adalah aplikasi web berbasis Flask yang menggunakan **Unsupervised Learning (K-Means Clustering)** untuk mengelompokkan kondisi tanah berdasarkan karakteristiknya. Sistem ini membantu mengidentifikasi pola dan kelompok kondisi tanah yang serupa tanpa memerlukan data berlabel.

## 📖 Tentang Website

### Apa itu SoilSense?

SoilSense adalah platform web interaktif yang memungkinkan pengguna untuk:
- **Menginput data kondisi tanah** (Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall)
- **Mendapatkan hasil clustering** yang menunjukkan kelompok kondisi tanah yang serupa
- **Melihat karakteristik cluster** untuk memahami pola kondisi tanah
- **Menghitung fertility score** berdasarkan kandungan nutrisi tanah

### Fitur Utama Website

1. **Input Form Interaktif**: Form yang user-friendly untuk memasukkan data kondisi tanah
2. **Real-time Clustering**: Hasil clustering langsung ditampilkan setelah input
3. **Visualisasi Hasil**: Menampilkan cluster assignment dan karakteristiknya
4. **Fertility Score Calculator**: Menghitung skor kesuburan tanah secara otomatis
5. **Responsive Design**: Dapat diakses dari berbagai perangkat (desktop, tablet, mobile)

## 🧠 Penerapan Unsupervised Learning di Website Ini

### Apa itu Unsupervised Learning?

**Unsupervised Learning** adalah teknik machine learning yang menemukan pola dalam data **tanpa menggunakan label atau target**. Berbeda dengan supervised learning yang membutuhkan contoh input-output, unsupervised learning hanya menggunakan fitur input untuk menemukan struktur tersembunyi dalam data.

### Mengapa Menggunakan Unsupervised Learning?

1. **Tidak Perlu Label Data**: Kita tidak perlu tahu sebelumnya tanaman apa yang cocok untuk setiap kondisi tanah
2. **Menemukan Pola Tersembunyi**: Dapat menemukan kelompok kondisi tanah yang tidak terduga
3. **Eksplorasi Data**: Membantu memahami struktur dan distribusi data
4. **Fleksibel**: Hasil clustering dapat digunakan untuk berbagai tujuan analisis

### Algoritma yang Digunakan: K-Means Clustering

**K-Means Clustering** adalah algoritma unsupervised learning yang mengelompokkan data ke dalam K cluster berdasarkan kemiripan fitur. Algoritma ini bekerja dengan cara:

1. **Inisialisasi**: Memilih K titik acak sebagai centroid awal
2. **Assignment**: Setiap data point ditugaskan ke cluster terdekat berdasarkan jarak Euclidean
3. **Update**: Menghitung ulang centroid sebagai rata-rata dari semua data point dalam cluster
4. **Iterasi**: Mengulangi langkah 2-3 sampai konvergen (centroid tidak berubah)

### Alur Penerapan di Website

#### 1. **Training Phase** (`train_model.py`)

```
Data Input (data_core.csv)
    ↓
Preprocessing (StandardScaler)
    ↓
Mencari Jumlah Cluster Optimal
    ├── Elbow Method
    └── Silhouette Score
    ↓
Training K-Means dengan K Optimal
    ↓
Evaluasi Model
    ├── Silhouette Score
    └── Davies-Bouldin Score
    ↓
Simpan Model & Cluster Info
    ├── model_cluster.pkl
    ├── scaler.pkl
    └── cluster_info.pkl
```

**Detail Proses Training:**

1. **Load Data**: Membaca dataset `data_core.csv` yang berisi 33,455 data kondisi tanah
2. **Preprocessing**: 
   - Menggunakan `StandardScaler` untuk normalisasi data
   - Memastikan semua fitur memiliki skala yang sama (mean=0, std=1)
3. **Optimal Cluster Selection**:
   - Mencoba K dari 2 sampai 10
   - Untuk setiap K, menghitung:
     - **Inertia**: Jumlah jarak kuadrat dari setiap data point ke centroid cluster-nya
     - **Silhouette Score**: Mengukur seberapa baik data point cocok dengan cluster-nya
   - Memilih K dengan Silhouette Score tertinggi
4. **Training K-Means**:
   - Melatih model dengan K optimal
   - Menghasilkan cluster labels untuk setiap data point
5. **Analisis Cluster**:
   - Menghitung karakteristik rata-rata setiap cluster
   - Menyimpan informasi cluster untuk digunakan di website

#### 2. **Prediction Phase** (`app.py`)

```
User Input (via Web Form)
    ↓
Preprocessing (StandardScaler)
    ↓
Predict Cluster (K-Means)
    ↓
Hitung Jarak ke Cluster Center
    ↓
Ambil Karakteristik Cluster
    ↓
Generate Description
    ↓
Return JSON Response
    ↓
Display di Frontend
```

**Detail Proses Prediction:**

1. **User Input**: Pengguna memasukkan 7 fitur kondisi tanah melalui form web
2. **Scaling**: Data input di-scale menggunakan scaler yang sama dengan training
3. **Cluster Prediction**: Model K-Means memprediksi cluster mana yang cocok
4. **Distance Calculation**: Menghitung jarak dari input ke cluster center (semakin kecil semakin mirip)
5. **Cluster Characteristics**: Mengambil karakteristik rata-rata cluster dari `cluster_info.pkl`
6. **Description Generation**: Membuat deskripsi otomatis berdasarkan karakteristik cluster
7. **Response**: Mengembalikan hasil dalam format JSON untuk ditampilkan di frontend

#### 3. **Frontend Display** (`templates/input_data.html` + `static/js/result.js`)

```
User Submit Form
    ↓
AJAX Request ke /predict
    ↓
Receive JSON Response
    ↓
Update UI
    ├── Cluster Name & Number
    ├── Cluster Description
    ├── Fertility Score
    └── Cluster Characteristics
```

### Teknis Implementasi

#### Backend (Flask)

```python
# Load model yang sudah ditraining
model_cluster = joblib.load("model_cluster.pkl")
scaler = joblib.load("scaler.pkl")
cluster_info = joblib.load("cluster_info.pkl")

# Predict cluster untuk input baru
df_scaled = scaler.transform(df_input)
cluster_pred = model_cluster.predict(df_scaled)[0]

# Ambil karakteristik cluster
cluster_characteristics = cluster_info.iloc[cluster_pred].to_dict()
```

#### Frontend (JavaScript)

```javascript
// Kirim data ke backend
const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
});

// Update UI dengan hasil clustering
predictedLabelElement.textContent = result.cluster_name;
cropDescriptionElement.textContent = result.cluster_description;
```

### Keuntungan Penerapan Unsupervised Learning

1. **Tidak Perlu Data Berlabel**: Dapat langsung menggunakan data mentah tanpa perlu tahu tanaman apa yang cocok
2. **Menemukan Pola Baru**: Dapat menemukan kelompok kondisi tanah yang tidak terduga
3. **Skalabel**: Mudah menambahkan data baru tanpa perlu re-labeling
4. **Interpretable**: Setiap cluster memiliki karakteristik yang jelas dan dapat dijelaskan

### Evaluasi Model

Website menggunakan beberapa metrik untuk mengevaluasi kualitas clustering:

1. **Silhouette Score** (Range: -1 sampai 1)
   - Semakin tinggi semakin baik
   - Mengukur seberapa baik data point cocok dengan cluster-nya
   - Nilai > 0.5 dianggap baik

2. **Davies-Bouldin Score**
   - Semakin rendah semakin baik
   - Mengukur rasio jarak intra-cluster dan inter-cluster

3. **Visualisasi PCA**
   - Menampilkan distribusi cluster dalam 2D
   - Membantu memahami struktur data

### Contoh Hasil Clustering

Setelah training, sistem akan menghasilkan beberapa cluster, misalnya:

- **Cluster 0**: Kondisi tanah dengan nitrogen tinggi, fosfor sedang, kalium rendah, suhu tinggi
- **Cluster 1**: Kondisi tanah dengan nitrogen sedang, fosfor tinggi, kalium tinggi, suhu rendah
- **Cluster 2**: Kondisi tanah dengan nitrogen rendah, fosfor rendah, kalium sedang, curah hujan tinggi
- dst...

Setiap cluster mewakili kelompok kondisi tanah yang memiliki karakteristik serupa.

## 📋 Prerequisites

Sebelum menjalankan project, pastikan sudah terinstall:

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Node.js & npm** (untuk Tailwind CSS) - [Download Node.js](https://nodejs.org/)

## 🚀 Cara Menjalankan Project

### Langkah 1: Install Dependencies Python

```bash
pip install -r requirements.txt
```

### Langkah 2: Install Dependencies Node.js (untuk Tailwind CSS)

```bash
npm install
```

### Langkah 3: Build CSS (jika belum ada file styles.css)

```bash
npm run build
```

**Catatan:** File `static/dist/styles.css` sudah ada, jadi langkah ini opsional.

### Langkah 4: Training Model Clustering

**PENTING**: Training model harus dilakukan sebelum menjalankan aplikasi web!

```bash
python train_model.py
```

**Estimasi Waktu**: Training memakan waktu sekitar **20-45 menit** tergantung spesifikasi komputer (dataset: 33,455 data points).

Proses training akan:
- ✅ Melatih model K-Means Clustering
- ✅ Mencari jumlah cluster optimal (mencoba K=2 sampai 10)
- ✅ Menghasilkan visualisasi di folder `hasil_train_plots/`:
  - Elbow Method & Silhouette Score plot
  - PCA Visualization (2D cluster distribution)
  - Cluster distribution chart
  - Cluster characteristics heatmap
  - Cluster characteristics bar chart
- ✅ Menyimpan model dan informasi:
  - `model_cluster.pkl` - Model K-Means
  - `scaler.pkl` - StandardScaler untuk preprocessing
  - `cluster_info.pkl` - Karakteristik setiap cluster
  - `cluster_centers.csv` - Data cluster centers

**Catatan**: Jika training terhenti atau error, pastikan semua dependencies terinstall dengan benar.

### Langkah 5: Jalankan Flask Application

```bash
python app.py
```

Server akan berjalan di: **http://127.0.0.1:5000** atau **http://localhost:5000**

### Langkah 6: Buka di Browser

Buka browser dan akses: **http://localhost:5000**

## 📁 Struktur Project

```
SoilSense-Predicting-System/
├── app.py                 # Flask application (main)
├── train_model.py         # Script training model clustering
├── data_core.csv          # Dataset training
├── model_cluster.pkl      # Model K-Means clustering
├── scaler.pkl            # StandardScaler untuk preprocessing
├── cluster_info.pkl       # Informasi karakteristik setiap cluster
├── cluster_centers.csv    # Data cluster centers
├── requirements.txt       # Dependencies Python
├── package.json          # Dependencies Node.js
├── templates/            # HTML templates
│   ├── index.html
│   └── input_data.html
└── static/               # Static files (CSS, JS, images)
    ├── dist/
    ├── js/
    └── assets/
```

## 🎯 Fitur Website

### 1. Input Data Kondisi Tanah
Pengguna dapat memasukkan 7 parameter kondisi tanah:
- **Nitrogen (N)**: Kandungan nitrogen dalam tanah (50-150)
- **Phosphorus (P)**: Kandungan fosfor dalam tanah (10-100)
- **Potassium (K)**: Kandungan kalium dalam tanah (10-100)
- **Temperature**: Suhu lingkungan (°C, 15-48)
- **Humidity**: Kelembaban udara (%, 20-100)
- **pH**: Tingkat keasaman tanah (4-8)
- **Rainfall**: Curah hujan (mm, 100-300)

### 2. Clustering Analysis
- **Automatic Cluster Assignment**: Sistem otomatis mengelompokkan input ke cluster yang sesuai
- **Cluster Characteristics**: Menampilkan karakteristik rata-rata cluster (tinggi/rendah nitrogen, suhu, dll)
- **Distance to Center**: Menghitung seberapa dekat input dengan pusat cluster

### 3. Fertility Score
- Menghitung skor kesuburan tanah menggunakan formula: `N × 0.4 + P × 0.3 + K × 0.3`
- Kategorisasi:
  - Very Low: 0 - 25.9
  - Low: 26.0 - 60.0
  - Moderate: 60.1 - 90.0
  - High: 90.1 - 120.0
  - Very High: 120.1+

### 4. Visualisasi Hasil
- Menampilkan nomor dan nama cluster
- Deskripsi karakteristik cluster dalam bahasa Indonesia
- Ikon visual untuk fertility score

## 🔧 Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### Error: Model file not found
Jalankan training model terlebih dahulu:
```bash
python train_model.py
```

**Catatan**: Setelah training, pastikan file berikut ada:
- `model_cluster.pkl`
- `scaler.pkl`
- `cluster_info.pkl`

### Port sudah digunakan
Edit `app.py` dan ubah port:
```python
app.run(debug=True, port=5001)  # Ganti port
```

## 📊 Informasi Model & Algoritma

### K-Means Clustering

**K-Means** adalah algoritma clustering yang membagi data menjadi K kelompok berdasarkan kemiripan fitur.

**Cara Kerja:**
1. Pilih K titik acak sebagai centroid awal
2. Assign setiap data point ke centroid terdekat
3. Update centroid sebagai rata-rata data point dalam cluster
4. Ulangi langkah 2-3 sampai konvergen

**Parameter Model:**
- `n_clusters`: Jumlah cluster (ditentukan otomatis berdasarkan Silhouette Score)
- `random_state`: 42 (untuk reproducibility)
- `n_init`: 10 (jumlah inisialisasi berbeda)

### Optimal Cluster Selection

Sistem menggunakan dua metode untuk menentukan jumlah cluster optimal:

1. **Elbow Method**: Mencari "siku" pada grafik inertia vs jumlah cluster
2. **Silhouette Score**: Memilih K dengan score tertinggi (range: -1 sampai 1)

**Hasil**: Sistem akan otomatis memilih K dengan Silhouette Score tertinggi dari range 2-10.

### Preprocessing

- **StandardScaler**: Normalisasi data agar semua fitur memiliki mean=0 dan std=1
- **Alasan**: Fitur memiliki skala berbeda (N: 50-150, P: 10-100, temperature: 15-48, dll)
- **Penting**: Input baru juga harus di-scale dengan scaler yang sama

### Evaluation Metrics

1. **Silhouette Score** (Range: -1 sampai 1)
   - > 0.5: Clustering baik
   - 0.2-0.5: Clustering wajar
   - < 0.2: Clustering buruk

2. **Davies-Bouldin Score**
   - Semakin rendah semakin baik
   - Mengukur rasio jarak intra-cluster dan inter-cluster

### Visualisasi

Website menghasilkan beberapa visualisasi selama training:

1. **Elbow Method & Silhouette Score Plot**: Menentukan K optimal
2. **PCA Visualization**: Distribusi cluster dalam 2D (Principal Component Analysis)
3. **Cluster Distribution**: Jumlah data per cluster
4. **Cluster Characteristics Heatmap**: Perbandingan karakteristik antar cluster
5. **Cluster Characteristics Bar Chart**: Visualisasi fitur per cluster

Semua visualisasi disimpan di folder `hasil_train_plots/`.

## 💡 Cara Menggunakan Website

### 1. Akses Website
Setelah menjalankan `python app.py`, buka browser dan akses: **http://localhost:5000**

### 2. Input Data
- Klik tombol untuk input data atau akses langsung ke halaman input
- Isi form dengan data kondisi tanah:
  - Gunakan titik (.) untuk angka desimal
  - Pastikan nilai dalam range yang disarankan (lihat info button)

### 3. Lihat Hasil
- Klik "Get Prediction"
- Sistem akan menampilkan:
  - **Soil Cluster**: Nomor dan nama cluster yang cocok
  - **Cluster Description**: Karakteristik cluster dalam bahasa Indonesia
  - **Fertility Score**: Skor kesuburan tanah dan kategorinya

### 4. Interpretasi Hasil
- **Cluster Number**: Menunjukkan kelompok kondisi tanah yang serupa
- **Cluster Description**: Menjelaskan karakteristik umum cluster (tinggi/rendah nitrogen, suhu, dll)
- **Fertility Score**: Indikator kesuburan tanah berdasarkan kandungan NPK

## 🔬 Penjelasan Teknis Unsupervised Learning

### Perbedaan dengan Supervised Learning

| Aspek | Supervised Learning | Unsupervised Learning (Website Ini) |
|-------|-------------------|-------------------------------------|
| **Data Input** | Fitur + Label | Hanya Fitur |
| **Tujuan** | Prediksi label baru | Menemukan pola/kelompok |
| **Output** | Klasifikasi/Regresi | Clustering |
| **Evaluasi** | Accuracy, Precision, Recall | Silhouette Score, Davies-Bouldin |
| **Use Case** | Prediksi tanaman spesifik | Eksplorasi pola kondisi tanah |

### Mengapa K-Means Cocok untuk Data Ini?

1. **Data Numerik**: Semua fitur adalah numerik (N, P, K, temperature, dll)
2. **Jumlah Cluster Tidak Diketahui**: Elbow Method & Silhouette Score membantu menentukan K optimal
3. **Spherical Clusters**: K-Means bekerja baik untuk cluster yang berbentuk bulat
4. **Skalabel**: Dapat menangani dataset besar (33K+ data points)

### Workflow Lengkap Sistem

```
┌─────────────────┐
│  Data Training   │
│  (data_core.csv) │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Preprocessing  │
│  (StandardScaler)│
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Find Optimal K  │
│ (Elbow + Silhouette)│
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Train K-Means   │
│  (n_clusters=K) │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Save Model      │
│ (model_cluster) │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Web App Ready  │
│   (app.py)      │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  User Input     │
│  (Web Form)     │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Predict Cluster │
│  (K-Means)      │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ Display Result  │
│  (Frontend)     │
└─────────────────┘
```

## 🛠️ Development

### Development Mode
```bash
python app.py
```
Flask sudah dalam debug mode, perubahan akan auto-reload.

### Testing Model
Untuk melihat hasil clustering pada data training:
```python
import joblib
import pandas as pd

# Load model
model = joblib.load("model_cluster.pkl")
scaler = joblib.load("scaler.pkl")
cluster_info = joblib.load("cluster_info.pkl")

# Load data
df = pd.read_csv("data_core.csv")
features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
X = df[features]
X_scaled = scaler.transform(X)

# Predict
clusters = model.predict(X_scaled)
print(f"Cluster distribution: {pd.Series(clusters).value_counts()}")
```

## 📚 Referensi

- **K-Means Clustering**: [Scikit-learn Documentation](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- **Silhouette Score**: Metrik untuk evaluasi clustering
- **PCA**: Principal Component Analysis untuk visualisasi

---

**Happy Coding! 🌱**

*Dibuat dengan ❤️ menggunakan Unsupervised Learning*

