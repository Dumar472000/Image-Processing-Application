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

# =================================== Structures ====================================
# ===================================================================================

################################################################### Erosion, dilation, opening & closing
def create_structuring_element_ellipse(width, height):
    """
    Create an elliptical structuring element using np.ogrid.

    Args:
        width (int): Width of the ellipse.
        height (int): Height of the ellipse.

    Returns:
        numpy.ndarray: Elliptical structuring element.
    """
    # Ensure non-zero dimensions for the ellipse
    width = max(width, 1)
    height = max(height, 1)

    # Create a square grid with side length twice the maximum of width and height plus one
    max_dim = max(width, height) // 2
    y, x = np.ogrid[-max_dim:max_dim + 1, -max_dim:max_dim + 1]

    # Use the equation of an ellipse: (x/a)^2 + (y/b)^2 = 1, where a = width/2, b = height/2
    ellipse = (x**2 / (width / 2)**2) + (y**2 / (height / 2)**2) <= 1

    return ellipse.astype(np.uint8)


def create_structuring_element_square(size):
    """
    Create a square structuring element.
    
    Args:
        size (int): Size of the square.
        
    Returns:
        numpy.ndarray: Square structuring element.
    """
    # Ensure size is at least 1 for the square structuring element
    size = max(size, 1)
    return np.ones((size, size), dtype=np.uint8)


def create_structuring_element_circle(radius):
    """
    Create a circular structuring element using np.ogrid.

    Args:
        radius (int): Radius of the circle.

    Returns:
        numpy.ndarray: Circular structuring element.
    """
    # Ensure non-zero radius
    radius = max(radius, 1)

    # Create a square grid with side length twice the radius plus one
    # basically creates x & y co-ordinate lists = [-n till n]
    y, x = np.ogrid[-radius:radius + 1, -radius:radius + 1]

    # Use the equation of a circle:  (x - h)^2 + (y - k)^2 = r^2, where (h, k) = centre, r = radius
    circle = x**2 + y**2 <= radius**2

    return circle.astype(np.uint8)


def create_structuring_element_diamond(size):
    """
    Create a diamond-shaped structuring element.

    Args:
        size (int): Size of the diamond.

    Returns:
        numpy.ndarray: Diamond-shaped structuring element.
    """
    # Ensure size is at least 1 for the diamond structuring element
    size = max(size, 1)
    
    center = size // 2

    # Create a grid representing the diamond
    y, x = np.ogrid[:size, :size]
    diamond = np.abs(x - center) + np.abs(y - center) <= center

    return diamond.astype(np.uint8)
    
    
def create_structuring_element_cross(size):
    """
    Create a cross-shaped structuring element.

    Args:
        size (int): Size of the cross.

    Returns:
        numpy.ndarray: Cross-shaped structuring element.
    """
    # Ensure size is at least 1 for the cross structuring element
    size = max(size, 1)

    cross = np.zeros((size, size), dtype=np.uint8)

    center = size // 2

    # Horizontal line
    cross[center, :] = 1
    # Vertical line
    cross[:, center] = 1

    return cross


def create_structuring_element_t(size):
    """
    Create a T-shaped structuring element.

    Args:
        size (int): Size of the T.

    Returns:
        numpy.ndarray: T-shaped structuring element.
    """
    # Ensure size is at least 1 for the T-shaped structuring element
    size = max(size, 1)

    t_shape = np.zeros((size, size), dtype=np.uint8)

    # Vertical line
    t_shape[:, size // 2] = 1
    # Horizontal line
    t_shape[0, :] = 1

    return t_shape


def create_structuring_element_slant(size, direction='left'):
    """
    Create a slanted line-shaped structuring element.

    Args:
        size (int): Size of the slanted line.
        direction (str): Direction of the slant ('left' or 'right').

    Returns:
        numpy.ndarray: Slanted line-shaped structuring element.
    """
    # Ensure size is at least 1 for the slanted line-shaped structuring element
    size = max(size, 1)

    slant_shape = np.zeros((size, size), dtype=np.uint8)

    if direction == 'left':
        for i in range(size):
            slant_shape[i, max(0, size - i - 1):] = 1
    elif direction == 'right':
        for i in range(size):
            slant_shape[i, :min(size, size - i)] = 1
    else:
        raise ValueError("Invalid direction. Supported directions are 'left' or 'right'.")

    return slant_shape


def create_structuring_element_polygon(size, sides):
    """
    Create a structuring element in the shape of a regular polygon.
    
    Args:
        size (int): The size of the square matrix (size x size).
        sides (int): The number of sides of the polygon.

    Returns:
        numpy.ndarray: Structuring element with the specified polygon.
    """
    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")
    size = max(size, 3)  # Ensure size is sufficient to form a polygon

    # Create an empty grid
    struct_elem = np.zeros((size, size), dtype=np.uint8)

    # Calculate the radius from the center of the matrix to a corner
    radius = size // 2

    # Center of the polygon
    center = (size // 2, size // 2)

    # Calculate the angle between vertices
    angle = 2 * np.pi / sides

    # Calculate the vertices of the polygon
    vertices = [(center[0] + radius * np.sin(i * angle), center[1] + radius * np.cos(i * angle)) for i in range(sides)]

    # Fill the polygon: ray-casting algorithm for point in polygon
    for y in range(size):
        for x in range(size):
            # Count intersections of the polygon with the ray from the point to the right
            intersections = 0
            for i in range(sides):
                j = (i + 1) % sides
                # Check if line from vertices[i] to vertices[j] intersects with ray from (x, y) horizontally
                if ((vertices[i][1] <= y < vertices[j][1]) or (vertices[j][1] <= y < vertices[i][1])):
                    # Compute the x coordinate of the intersection
                    intersect_x = vertices[i][0] + (y - vertices[i][1]) * (vertices[j][0] - vertices[i][0]) / (vertices[j][1] - vertices[i][1])
                    if intersect_x > x:
                        intersections += 1

            # Inside the polygon if intersections is odd
            if intersections % 2 == 1:
                struct_elem[y, x] = 1

    return struct_elem


def create_custom_structuring_element(shape, *args):
    """
    Create a custom structuring element based on the specified shape.

    Args:
        shape (str): The shape of the structuring element. Options: 'ellipse', 'square', 'circle', 'diamond', 'cross', 't', 'slant', 'polygon'.

    Additional Parameters:
        For 'ellipse': width (int), height (int).
        For 'square': size (int).
        For 'circle': radius (int).
        For 'diamond': size (int).
        For 'cross': size (int).
        For 't': size (int).
        For 'slant': size (int), direction (str: 'left' or 'right').
        For 'polygon': size (int), sides (int).

    Returns:
        numpy.ndarray: Custom structuring element.
    """
    # will also read if data is not formatted correctly e.g ElliPsE or sQuaRE etc
    shape = shape.lower()
    
    if shape == 'ellipse':
        return create_structuring_element_ellipse(*args)
    elif shape == 'square':
        return create_structuring_element_square(*args)
    elif shape == 'circle':
        return create_structuring_element_circle(*args)
    elif shape == 'diamond':
        return create_structuring_element_diamond(*args)
    elif shape == 'cross':
        return create_structuring_element_cross(*args)
    elif shape == 't':
        return create_structuring_element_t(*args)
    elif shape == 'slant':
        return create_structuring_element_slant(*args)
    elif shape == 'polygon':
        return create_structuring_element_polygon(*args)
    else:
        raise ValueError("Invalid shape. Supported shapes are: 'ellipse', 'square', 'circle', 'diamond', 'cross', 't', 'slant', 'polygon'.")


# ==================================== Morphology ===================================
# ===================================================================================

########################################################## Morphological Operations
def erosion(image, structuring_element):
    """
    Perform erosion operation on a binary image using vectorized operations.
    
    Args:
        image: Binary input image (grayscale)
        structuring_element: Structuring element for erosion
    
    Returns:
        Eroded image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Convert to binary (0 or 1) for easier processing
    binary_image = (image > 127).astype(np.uint8)
    
    # Get dimensions
    img_height, img_width = binary_image.shape
    se_height, se_width = structuring_element.shape
    
    # Calculate padding
    pad_h = se_height // 2
    pad_w = se_width // 2
    
    # Pad the image with zeros (background)
    padded_image = np.pad(binary_image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    # Use sliding window view for vectorized operation
    shape = (img_height, img_width, se_height, se_width)
    strides = padded_image.strides + padded_image.strides
    windows = np.lib.stride_tricks.as_strided(padded_image, shape=shape, strides=strides)
    
    # Reshape structuring element for broadcasting
    se_reshaped = structuring_element.reshape(1, 1, se_height, se_width)
    
    # For erosion: check if ALL positions where SE=1 have image=1
    # Create mask where structuring element is 1
    se_mask = (se_reshaped == 1)
    
    # Apply erosion condition: where SE=1, image must be 1
    erosion_condition = np.where(se_mask, windows, 1)  # Set non-SE positions to 1 (don't affect result)
    
    # Check if all SE positions are satisfied
    eroded = np.all(erosion_condition == 1, axis=(2, 3)).astype(np.uint8)
    
    # Convert back to 0-255 range
    return eroded * 255


def dilation(image, structuring_element):
    """
    Perform dilation operation on a binary image using vectorized operations.
    
    Args:
        image: Binary input image (grayscale)
        structuring_element: Structuring element for dilation
    
    Returns:
        Dilated image
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = np.dot(image[...,:3], [0.2989, 0.5870, 0.1140])
        image = image.astype(np.uint8)
    else:
        image = image.astype(np.uint8)
    
    # Convert to binary (0 or 1) for easier processing
    binary_image = (image > 127).astype(np.uint8)
    
    # Get dimensions
    img_height, img_width = binary_image.shape
    se_height, se_width = structuring_element.shape
    
    # Calculate padding
    pad_h = se_height // 2
    pad_w = se_width // 2
    
    # Pad the image with zeros (background)
    padded_image = np.pad(binary_image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    # Use sliding window view for vectorized operation
    shape = (img_height, img_width, se_height, se_width)
    strides = padded_image.strides + padded_image.strides
    windows = np.lib.stride_tricks.as_strided(padded_image, shape=shape, strides=strides)
    
    # Reshape structuring element for broadcasting
    se_reshaped = structuring_element.reshape(1, 1, se_height, se_width)
    
    # For dilation: check if ANY position where SE=1 AND image=1
    # Create mask where both SE=1 and image=1
    overlap = (windows == 1) & (se_reshaped == 1)
    
    # Check if any SE position overlaps with foreground
    dilated = np.any(overlap, axis=(2, 3)).astype(np.uint8)
    
    # Convert back to 0-255 range
    return dilated * 255


def opening(image, structuring_element):
    """
    Perform opening operation (erosion followed by dilation).
    
    Args:
        image: Binary input image
        structuring_element: Structuring element for opening
    
    Returns:
        Opened image
    """
    eroded = erosion(image, structuring_element)
    opened = dilation(eroded, structuring_element)
    return opened


def closing(image, structuring_element):
    """
    Perform closing operation (dilation followed by erosion).
    
    Args:
        image: Binary input image
        structuring_element: Structuring element for closing
    
    Returns:
        Closed image
    """
    dilated = dilation(image, structuring_element)
    closed = erosion(dilated, structuring_element)
    return closed
