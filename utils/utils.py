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

# Numpy Sliding Tricks
from numpy.lib.stride_tricks import as_strided

# Other Necessary Libraries
import numpy as np

# ==================================== Utilities ====================================
# ===================================================================================

# For Convulution
def convolve(image, kernel):
    # Get the dimensions of the image and the kernel
    image_height, image_width = image.shape
    kernel_height, kernel_width = kernel.shape
    
    # Calculate output dimensions
    output_height = image_height - kernel_height + 1
    output_width = image_width - kernel_width + 1
    
    # Create strides for the image
    image_strides = image.strides
    
    # Calculate strides for a sliding window of the image
    window_strides = (image_strides[0], image_strides[1], *image_strides)
    
    # Create a view of the image with shape (output_height, output_width, kernel_height, kernel_width)
    image_view = as_strided(image, shape=(output_height, output_width, kernel_height, kernel_width),
                            strides=(window_strides[0], window_strides[1], *image_strides))
    
    # Perform element-wise multiplication between the image view and the kernel
    convolved = np.tensordot(image_view, kernel, axes=((2,3), (0,1)))
    
    return convolved.astype(np.uint8)


# Convert BGR to YUV using numpy
def bgr_to_yuv(image):
    image = np.array(image)
    # Conversion matrix from BGR to YUV
    conversion_matrix = np.array([[0.299, 0.587, 0.114],
                                  [-0.14713, -0.28886, 0.436],
                                  [0.615, -0.51499, -0.10001]])
    yuv_image = np.dot(image.astype(np.float32), conversion_matrix.T)
    yuv_image[:, :, 1:] += 128  # Shift chrominance values
    return yuv_image.astype(np.uint8)

# Convert YUV to BGR using numpy
def yuv_to_bgr(image):
    image = np.array(image)
    # Conversion matrix from YUV to BGR
    conversion_matrix = np.array([[1.0, 0.0, 1.13983],
                                  [1.0, -0.39465, -0.58060],
                                  [1.0, 2.03211, 0.0]])
    image[:, :, 1:] -= 128  # Shift chrominance values
    bgr_image = np.dot(image.astype(np.float32), conversion_matrix.T)
    return np.clip(bgr_image, 0, 255).astype(np.uint8)

# Function to convert rgb image to graysacle (taken from the internet)
def rgb_to_gray(image):
    # Convert RGB image to grayscale using the formula: gray = 0.299*R + 0.5869*G + 0.114*B
    return np.dot(image[..., :3], [0.299, 0.5869, 0.114]).astype(np.uint8)
