from PIL import Image
from numpy import asarray, uint8, argsort
from sklearn.cluster import KMeans
from collections import Counter


class ExtractColors:
    def __init__(self):
        self.colors_hex = []
        self.color_percent = []
        self.num_colors = 10

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

    def extract_dominant_colors(self, image_path):
        # Open the image file
        img = Image.open(image_path)
        img = img.convert("RGB")
        ar = asarray(img)
        # Reshape the image array to have a shape of (num_pixels, 3)
        reshaped_image = ar.reshape(-1, 3)
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=self.num_colors, random_state=42)
        labels = kmeans.fit_predict(reshaped_image)
        # Get the cluster centers (representative colors)
        cluster_centers = kmeans.cluster_centers_
        # Convert the cluster centers to uint8 and reshape
        dominant_colors = cluster_centers.astype(uint8).reshape(-1, 3)
        # Convert the dominant colors to hex format
        colors_hex = [self.rgb_to_hex(color) for color in dominant_colors]
        # Count occurrences of each cluster
        cluster_counts = Counter(labels)
        total_occurrences = sum(cluster_counts.values())
        color_counter = list(cluster_counts.values())
        color_percent = [round(int(occ) * 100 / total_occurrences) for occ in color_counter]
        color_percent = asarray(color_percent)
        colors_hex = asarray(colors_hex)
        sort_indices = argsort(-color_percent)
        self.colors_hex = colors_hex[sort_indices]
        self.color_percent = color_percent[sort_indices]
        return self.colors_hex, self.color_percent

    def reset_extract_colors(self):
        self.colors_hex = []
        self.color_percent = []
