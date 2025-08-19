# Copyright 2025 Ahmed Kamal
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ================================== All Libraries ==================================
# ===================================================================================

# Import utilities
from utils.utils import convolve

# For Image Manipulation
import cv2

# Other Necessary Libraries
import numpy as np

# =============================== Advanced Algorithms ===============================
# ===================================================================================

########################################################## Laplacian of Gaussian (LOG)
def gaussian_kernel(size, sigma = 1.0):
    """Return N-Dimensional Gaussian Kernel
    @param integer  size  size of kernel / will be round to a nearest odd number
    @param float    sigma standard deviation of gaussian
    """
    s = int(size / 2)
    x, y = np.mgrid[-s:s+1, -s:s+1]
    k = np.exp(-(np.power(x, 2) + np.power(y, 2)) / (2 * (sigma ** 2)))
    return k / k.sum()

def laplacian_kernel():
    """Returns a 3x3 Laplacian kernel."""
    return np.array([[0, 1, 0],
                     [1, -4, 1],
                     [0, 1, 0]])

def laplacian_of_gaussian(image, kernel_size):
    image = np.array(image)
    image = image[:, :, :3]
    
    # Convert to grayscale
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Ensure kernel size is odd to have a central pixel
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8  # Calculation as used in OpenCV
    
    # Step 1: Apply Gaussian blur
    gaussian = gaussian_kernel(kernel_size, sigma)
    blurred_image = convolve(image, gaussian)
    
    # Step 2: Apply Laplacian filter
    laplacian = laplacian_kernel()
    log_image = convolve(blurred_image, laplacian)
    
    return log_image.astype(np.uint8)


########################################################## Colour Clustering (Using K-means)
def initialize_centroids(pixels, k):
    indices = np.random.choice(pixels.shape[0], k, replace=False)
    return pixels[indices]

def assign_clusters(pixels, centroids):
    distances = np.linalg.norm(pixels[:, np.newaxis] - centroids, axis=2)
    return np.argmin(distances, axis=1)

def recalculate_centroids(pixels, labels, k):
    centroids = np.array([pixels[labels == i].mean(axis=0) if np.any(labels == i) else pixels[np.random.choice(pixels.shape[0])] for i in range(k)])
    return centroids

def k_means(pixels, k=4, max_iters=100):
    centroids = initialize_centroids(pixels, k)
    for _ in range(max_iters):
        labels = assign_clusters(pixels, centroids)
        new_centroids = recalculate_centroids(pixels, labels, k)
        if np.allclose(centroids, new_centroids, atol=1e-4):
            break
        centroids = new_centroids
    return centroids, labels

def perform_color_clustering(image, num_clusters = 4):
    # Load the image
    img_data = np.array(image)
    img_data = img_data[:, :, :3]

    # Reshape the image data into a two-dimensional array
    pixels = img_data.reshape(-1, 3)

    # Apply k-means clustering
    centroids, labels = k_means(pixels, k=num_clusters)
    new_colors = centroids[labels].astype(np.uint8)

    # Reshape back to the original image shape
    new_image_data = new_colors.reshape(img_data.shape)

    return new_image_data.astype(np.uint8)


########################################################## Image Segmentation (generic)
def segment_image(image):
    # If image = 4D, get only 3 channels
    image = np.array(image)
    image = image[:, :, :3]
    
     # Convert to grayscale
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        gray_image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        gray_image = gray_image.astype(np.uint8)
    else:
        gray_image = image.astype(np.uint8)

    # Apply Gaussian blur to reduce noise (predefined gaussian blur)
    gaussian_k = gaussian_kernel(5, 1.0)
    blurred_image = convolve(gray_image, gaussian_k)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred_image, 50, 100)

    # Apply morphological operations to enhance edges
    kernel = np.ones((5, 5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    min_area = 1000  # Minimum contour area threshold
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # Create a mask of zeros
    mask = np.zeros_like(gray_image)

    # Draw contours on the mask
    cv2.drawContours(mask, filtered_contours, -1, (255), thickness=cv2.FILLED)

    # Fill holes in the mask
    mask_filled = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Bitwise AND operation to extract segmented object
    segmented_object = cv2.bitwise_and(image, image, mask=mask_filled)
    
    return segmented_object.astype(np.uint8)
