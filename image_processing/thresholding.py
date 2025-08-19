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

# =================================== Thresholding ==================================
# ===================================================================================

########################################################## THRESHOLDING
########################################################## BINARY_OTSU
def Binary_OTSU(image):
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)

    # Set total number of bins in the histogram
    bins_num = 256
    is_normalized = True

    # Get the image histogram
    hist, bin_edges = np.histogram(image, bins=bins_num)

    # Get normalized histogram if it is required
    if is_normalized:
        hist = np.divide(hist.ravel(), hist.max())

    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

    # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]

    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    # Maximize the inter_class_variance function val
    index_of_max_val = np.argmax(inter_class_variance)

    threshold = bin_mids[:-1][index_of_max_val]
    print("Otsu's algorithm implementation thresholding result: ", threshold)
    binary_image = np.where(image > threshold, 255, 0).astype(np.uint8)
    return binary_image

########################################################## Adaptive Thresholding
def adaptive_thresholding(image, block_size = 3, C = 2):
    if len(image.shape) == 3 and image.shape[2] == 3:
        # Assuming the image is RGB, convert it to grayscale
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Ensure the block size is odd
    if block_size % 2 == 0:
        block_size += 1

    # Compute the shape and strides
    pad_size = block_size // 2
    padded_image = np.pad(image, pad_size, mode='reflect')
    shape = (image.shape[0], image.shape[1], block_size, block_size)
    strides = padded_image.strides[:2] + padded_image.strides[:2]
    
    # Create a strided array of local blocks
    local_blocks = as_strided(padded_image, shape=shape, strides=strides)
    local_means = local_blocks.mean(axis=(2, 3))

    # Apply the thresholding
    thresholded_image = np.where(image > local_means - C, 255, 0).astype(np.uint8)

    return thresholded_image

########################################################## Simple Thresholding
def simple_thresholding(image, threshold):
    # Apply simple thresholding
    thresholded_image = np.where(image > threshold, 255, 0)
    
    return thresholded_image.astype(np.uint8)
