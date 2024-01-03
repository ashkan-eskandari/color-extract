# from PIL import Image
# from numpy import asarray, uint8, argsort
# from sklearn.cluster import KMeans
# from collections import Counter
#
#
# class ExtractColors:
#     def __init__(self):
#         self.colors_hex = []
#         self.color_percent = []
#         self.num_colors = 10
#
#     def rgb_to_hex(self, rgb):
#         return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
#
#     def extract_dominant_colors(self, image_path):
#         # Open the image file
#         img = Image.open(image_path)
#         img = img.convert("RGB")
#         ar = asarray(img)
#         # Reshape the image array to have a shape of (num_pixels, 3)
#         reshaped_image = ar.reshape(-1, 3)
#         # Perform K-means clustering
#         kmeans = KMeans(n_clusters=self.num_colors, random_state=42)
#         labels = kmeans.fit_predict(reshaped_image)
#         # Get the cluster centers (representative colors)
#         cluster_centers = kmeans.cluster_centers_
#         # Convert the cluster centers to uint8 and reshape
#         dominant_colors = cluster_centers.astype(uint8).reshape(-1, 3)
#         # Convert the dominant colors to hex format
#         colors_hex = [self.rgb_to_hex(color) for color in dominant_colors]
#         # Count occurrences of each cluster
#         cluster_counts = Counter(labels)
#         total_occurrences = sum(cluster_counts.values())
#         color_counter = list(cluster_counts.values())
#         color_percent = [round(int(occ) * 100 / total_occurrences) for occ in color_counter]
#         color_percent = asarray(color_percent)
#         colors_hex = asarray(colors_hex)
#         sort_indices = argsort(-color_percent)
#         self.colors_hex = colors_hex[sort_indices]
#         self.color_percent = color_percent[sort_indices]
#         return self.colors_hex, self.color_percent
#
#     def reset_extract_colors(self):
#         self.colors_hex = []
#         self.color_percent = []
from PIL import Image
import numpy as np
from collections import Counter


class ExtractColors:
    def __init__(self):
        self.colors_hex = []
        self.color_percent = []
        self.num_colors = 10

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def basic_kmeans(self, data, k, max_iterations=100):
        # Randomly initialize centroids
        centroids = data[np.random.choice(len(data), k, replace=False)]

        for _ in range(max_iterations):
            # Assign each data point to the nearest centroid
            labels = np.argmin(np.linalg.norm(data - centroids[:, np.newaxis], axis=2), axis=0)

            # Update centroids based on the mean of points assigned to each cluster
            new_centroids = np.array([np.mean(data[labels == i], axis=0) for i in range(k)])

            # Check for convergence
            if np.all(centroids == new_centroids):
                break

            centroids = new_centroids

        return labels

    def extract_dominant_colors(self, image_path):
        # Open the image file
        img = Image.open(image_path)
        img = img.convert("RGB")
        ar = np.asarray(img)
        # Reshape the image array to have a shape of (num_pixels, 3)
        reshaped_image = ar.reshape(-1, 3)

        # Perform basic K-means clustering
        labels = self.basic_kmeans(reshaped_image, self.num_colors)

        # Get the cluster centers (representative colors)
        cluster_centers = np.array([np.mean(reshaped_image[labels == i], axis=0) for i in range(self.num_colors)])

        dominant_colors = cluster_centers.astype(np.uint8)
        colors_hex = [self.rgb_to_hex(color) for color in dominant_colors]

        cluster_counts = Counter(labels)
        total_occurrences = sum(cluster_counts.values())
        color_counter = list(cluster_counts.values())
        color_percent = [round(int(occ) * 100 / total_occurrences) for occ in color_counter]
        color_percent = np.asarray(color_percent)

        sort_indices = np.argsort(-color_percent)
        self.colors_hex = np.asarray(colors_hex)[sort_indices]
        self.color_percent = color_percent[sort_indices]

        return self.colors_hex, self.color_percent

    def reset_extract_colors(self):
        self.colors_hex = []
        self.color_percent = []



