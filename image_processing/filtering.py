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

# Other Necessary Libraries
import numpy as np

# ==================================== Filtering ====================================
# ===================================================================================

########################################################## Filtering
########################################################## Average
def apply_averaging_filter(image, kernel_size):
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    # Define the averaging kernel
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size ** 2)

    # Pad the image to handle border pixels
    padding = kernel_size // 2
    padded_image = np.pad(image, padding, mode='constant')

    # Create strided view for efficient convolution
    convolved_image = np.lib.stride_tricks.sliding_window_view(padded_image, (kernel_size, kernel_size))

    # Perform convolution
    filtered_image = np.tensordot(convolved_image, kernel, axes=((-2, -1), (0, 1)))

    return filtered_image.astype(np.uint8)

########################################################## Laplacian
def laplacian_filter(image, kernel_size):
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    # Define Laplacian kernel
    kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) * -1
    kernel[kernel_size//2, kernel_size//2] = kernel_size**2 - 1

    # Pad the image to handle borders
    padded_image = np.pad(image, ((kernel_size//2, kernel_size//2), (kernel_size//2, kernel_size//2)), mode='constant')

    # Extract patches from the padded image using stride tricks
    patches = np.lib.stride_tricks.sliding_window_view(padded_image, (kernel_size, kernel_size))

    # Perform element-wise multiplication and sum along the last two axes
    filtered_image = np.sum(patches * kernel, axis=(-2, -1))
    
    # Convert to uint8
    filtered_image = np.uint8(np.absolute(filtered_image))

    return filtered_image

########################################################## Median
def apply_median_filter(image, kernel_size):
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    # Pad the image to handle borders
    pad_width = kernel_size // 2
    padded_image = np.pad(image, pad_width, mode='constant')
    
    # Determine the dimensions of the padded image
    height, width = padded_image.shape
    
    # Extract patches from the padded image using array slicing
    patches = np.lib.stride_tricks.sliding_window_view(padded_image, (kernel_size, kernel_size))
    
    # Reshape patches to make them suitable for median calculation
    reshaped_patches = patches.reshape(-1, kernel_size * kernel_size)
    
    # Calculate median for each patch
    median_values = np.median(reshaped_patches, axis=1)
    
    # Reshape the median values to match the original image dimensions
    median_image = median_values.reshape(height - kernel_size + 1, width - kernel_size + 1)
    
    return median_image.astype(np.uint8)
