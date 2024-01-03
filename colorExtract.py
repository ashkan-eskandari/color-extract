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
        centroids = data[np.random.choice(len(data), k, replace=False)]

        for _ in range(max_iterations):
            labels = np.argmin(np.linalg.norm(data - centroids[:, np.newaxis], axis=2), axis=0)
            new_centroids = np.array([np.mean(data[labels == i], axis=0) for i in range(k)])
            if np.all(centroids == new_centroids):
                break
            centroids = new_centroids
        return labels

    def extract_dominant_colors(self, image_path):
        img = Image.open(image_path)
        img = img.convert("RGB")
        ar = np.asarray(img)
        reshaped_image = ar.reshape(-1, 3)
        labels = self.basic_kmeans(reshaped_image, self.num_colors)
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



