import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
import joblib

# Tentukan folder penyimpanan plot
folder_plots = "hasil_train_plots"
if not os.path.exists(folder_plots):
    os.makedirs(folder_plots)

# Load data
df = pd.read_csv("data_core.csv")
print(df.head())
print(df.info())
print(df.describe())

# Fitur numerik
features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']

# Histogram distribusi
plt.figure(figsize=(15, 10))
for i, feature in enumerate(features):
    plt.subplot(3, 3, i+1)
    sns.histplot(df[feature], kde=True)
    plt.title(f'Distribusi {feature}')
plt.tight_layout()
plt.savefig(os.path.join(folder_plots, "plot_histogram_distribusi.png"))
plt.close()

# Heatmap korelasi
corr = df[features].corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriks Korelasi Fitur Numerik')
plt.savefig(os.path.join(folder_plots, "plot_korelasi_heatmap.png"))
plt.close()

# Pairplot (tanpa label karena unsupervised)
sns.pairplot(df[features])
plt.savefig(os.path.join(folder_plots, "plot_pairplot.png"))
plt.close()

# Skew dan Kurtosis
numeric_df = df.select_dtypes(include=['number'])
print("Skewness:\n", numeric_df.skew())
print("Kurtosis:\n", numeric_df.kurt())

# Missing value check
missing_values = df.isnull().sum()
print("Missing values:\n", missing_values[missing_values > 0])

# Boxplot per fitur (independen dari label)
plt.figure(figsize=(15,10))
for i, feature in enumerate(features):
    plt.subplot(3, 3, i+1)
    sns.boxplot(y=df[feature])
    plt.title(f'Boxplot {feature}')
plt.tight_layout()
plt.savefig(os.path.join(folder_plots, "plot_boxplot_all_features.png"))
plt.close()

# Persiapan data untuk unsupervised learning
X = df[features]

# Scaling data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Dataset shape: {X_scaled.shape}")
print(f"Number of features: {len(features)}")

# Menentukan jumlah cluster optimal menggunakan Elbow Method dan Silhouette Score
print("\n[INFO] Mencari jumlah cluster optimal...")
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

# Plot Elbow Method
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.grid(True)

# Plot Silhouette Score
plt.subplot(1, 2, 2)
plt.plot(K_range, silhouette_scores, 'ro-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(folder_plots, "plot_optimal_clusters.png"))
plt.close()

# Pilih jumlah cluster dengan silhouette score tertinggi
optimal_k = K_range[np.argmax(silhouette_scores)]
print(f"[INFO] Jumlah cluster optimal: {optimal_k} (Silhouette Score: {max(silhouette_scores):.4f})")

# Training K-Means dengan jumlah cluster optimal
print(f"\n[INFO] Training K-Means dengan {optimal_k} clusters...")
kmeans_model = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans_model.fit_predict(X_scaled)

# Evaluasi clustering
silhouette_avg = silhouette_score(X_scaled, cluster_labels)
davies_bouldin = davies_bouldin_score(X_scaled, cluster_labels)

print(f"[INFO] Silhouette Score: {silhouette_avg:.4f}")
print(f"[INFO] Davies-Bouldin Score: {davies_bouldin:.4f}")

# Tambahkan cluster labels ke dataframe untuk analisis
df['cluster'] = cluster_labels

# Visualisasi distribusi cluster
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='cluster')
plt.title('Distribusi Data per Cluster')
plt.xlabel('Cluster')
plt.ylabel('Jumlah Data')
plt.savefig(os.path.join(folder_plots, "plot_distribusi_cluster.png"))
plt.close()

# Visualisasi cluster dengan PCA (2D projection)
from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(10, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, cmap='viridis', alpha=0.6)
plt.scatter(pca.transform(kmeans_model.cluster_centers_)[:, 0], 
            pca.transform(kmeans_model.cluster_centers_)[:, 1], 
            c='red', marker='x', s=200, linewidths=3, label='Centroids')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
plt.title('K-Means Clustering (PCA Visualization)')
plt.colorbar(scatter, label='Cluster')
plt.legend()
plt.savefig(os.path.join(folder_plots, "plot_clustering_pca.png"))
plt.close()

# Analisis karakteristik setiap cluster
print("\n[INFO] Karakteristik Cluster:")
cluster_centers_original = scaler.inverse_transform(kmeans_model.cluster_centers_)
cluster_info = pd.DataFrame(cluster_centers_original, columns=features)
cluster_info.index = [f'Cluster {i}' for i in range(optimal_k)]
print(cluster_info)

# Visualisasi karakteristik cluster
plt.figure(figsize=(12, 8))
cluster_info.T.plot(kind='bar', figsize=(12, 8))
plt.title('Karakteristik Rata-rata Fitur per Cluster')
plt.xlabel('Fitur')
plt.ylabel('Nilai')
plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(folder_plots, "plot_karakteristik_cluster.png"))
plt.close()

# Heatmap karakteristik cluster
plt.figure(figsize=(10, 6))
sns.heatmap(cluster_info, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Nilai Rata-rata'})
plt.title('Heatmap Karakteristik Cluster')
plt.ylabel('Cluster')
plt.xlabel('Fitur')
plt.tight_layout()
plt.savefig(os.path.join(folder_plots, "plot_heatmap_cluster.png"))
plt.close()

# Simpan model dan informasi cluster
joblib.dump(kmeans_model, "model_cluster.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(cluster_info, "cluster_info.pkl")

# Simpan cluster centers untuk referensi
cluster_centers_df = pd.DataFrame(cluster_centers_original, columns=features)
cluster_centers_df.to_csv("cluster_centers.csv", index=False)

print("\n[INFO] Training selesai. Model clustering dan plot berhasil disimpan.")
print(f"[INFO] Model disimpan: model_cluster.pkl")
print(f"[INFO] Scaler disimpan: scaler.pkl")
print(f"[INFO] Informasi cluster disimpan: cluster_info.pkl")
print(f"[INFO] Cluster centers disimpan: cluster_centers.csv")