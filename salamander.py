import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def generate_points_around_center(latitude, longitude, num_points=10000, radius_miles=1):
    R = 6371
    r = radius_miles * 1.60934 / R
    
    deltas = np.sqrt(np.random.uniform(0, r**2, num_points))
    thetas = np.random.uniform(0, 2 * np.pi, num_points)

    lat_deltas = deltas * np.sin(thetas)
    lon_deltas = deltas * np.cos(thetas) / np.cos(latitude)
    
    lats = latitude + lat_deltas * (180/np.pi)
    lons = longitude + lon_deltas * (180/np.pi)
    
    return np.column_stack((lats, lons))

# Generate random coordinates
center_latitude = 40.7128
center_longitude = -74.0060
coordinates = generate_points_around_center(center_latitude, center_longitude)

# Scale the data
scaled_coordinates = StandardScaler().fit_transform(coordinates)

# Perform DBSCAN clustering
db = DBSCAN(eps=0.05, min_samples=10).fit(scaled_coordinates)
labels = db.labels_

# Identify the largest cluster
cluster_ids, cluster_sizes = np.unique(labels[labels != -1], return_counts=True)
largest_cluster_id = cluster_ids[np.argmax(cluster_sizes)]
largest_cluster_coords = coordinates[labels == largest_cluster_id]
cluster_centroid = largest_cluster_coords.mean(axis=0)

# Compute the entire dataset's centroid and standard deviation
data_centroid = coordinates.mean(axis=0)
data_std = coordinates.std(axis=0)

# Calculate the Euclidean distance between the cluster centroid and the data centroid
distance = np.linalg.norm(cluster_centroid - data_centroid)

# Calculate z-score using the combined standard deviations
z_score = distance / np.linalg.norm(data_std)

# Plotting
plt.scatter(coordinates[:,1], coordinates[:,0], c=labels, s=5, cmap='rainbow', alpha=0.5)
plt.scatter(cluster_centroid[1], cluster_centroid[0], c='black', s=100, marker='x', label='Cluster Centroid')
plt.title('DBSCAN Clustering')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()

print(f"Centroid of the largest cluster: Latitude {cluster_centroid[0]:.4f}, Longitude {cluster_centroid[1]:.4f}")
print(f"Z-score of the cluster: {z_score:.4f}")
