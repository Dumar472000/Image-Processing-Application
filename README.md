# Digital Image Processing Studio

A powerful desktop application for image processing and manipulation built with Python and PyQt5.

## What This App Does

This tool lets you work with images in many different ways. You can load photos, apply filters, adjust brightness and contrast, and perform advanced image processing operations. The app has a clean, modern interface that makes image editing (not really, but could say so) easy and fun.

## Features

### Image Loading
- Open regular image files (PNG, JPG, JPEG)
- Load images from PDF documents
- Work with video files frame by frame
- Drag and drop support for quick file loading

### Basic Image Operations
- **Brightness Control**: Make images lighter or darker
- **Contrast Adjustment**: Enhance image contrast using multiplication or power functions
- **Image Resizing**: Change image dimensions
- **Rotation**: Rotate images 90 degrees
- **Mirroring**: Flip images horizontally or vertically

### Filtering Options
- **Average Filter**: Smooth out image noise
- **Median Filter**: Remove salt-and-pepper noise
- **Laplacian Filter**: Detect edges and sharpen images

### Advanced Processing
- **Histogram Equalization**: Improve image contrast automatically
  - Global histogram equalization
  - Adaptive histogram equalization for better local contrast
- **Thresholding**: Convert images to black and white
  - Binary OTSU thresholding (automatic)
  - Simple value-based thresholding
  - Adaptive thresholding
- **Morphological Operations**: Shape-based image processing
  - Erosion and dilation
  - Opening and closing operations
  - Custom structuring elements (square, circle, diamond, etc.)
- **Clustering**: Group similar colors together
- **Image Segmentation**: Separate objects from background
- **Laplacian of Gaussian**: Advanced edge detection

### User Interface
- Split-screen view showing original and processed images
- Animated preview panel with dynamic patterns
- Separate windows for large images (before/after comparison)
- Modern dark theme with gradient styling
- Easy-to-use dropdown menu for function selection

## How to Run

### Requirements
Make sure you have Python installed on your computer. You'll also need these packages:

```bash
pip install PyQt5 numpy opencv-python pdf2image scipy
```

### Starting the App
1. Open your terminal or command prompt
2. Navigate to the project folder
3. Run this command:
```bash
python main.py
```

The app window will open and you can start using it right away.

## How to Use

1. **Load an Image**: Click "Select Image" to choose a file from your computer
2. **Pick a Function**: Use the dropdown menu to select what you want to do
3. **Process the Image**: Click "Process Image" to apply the selected operation
4. **Save Your Work**: Use "Save Image" to export the processed image

For operations like filters and thresholding, dialog boxes will appear with additional options. Just follow the prompts to customize the settings.

## Project Structure

The code is organized into several folders:

- `gui/` - User interface components
  - `app.py` - Main application window
  - `dialogs.py` - Settings dialogs for different operations
  - `assets/` - Image files and resources
- `image_processing/` - Core image processing functions
  - `filtering.py` - Image filters
  - `enhancing.py` - Histogram operations
  - `thresholding.py` - Thresholding methods
  - `morphology.py` - Morphological operations
  - `advanced.py` - Complex processing algorithms
- `utils/` - Helper functions and utilities
- `main.py` - Application entry point

## Technical Details

This application uses several key technologies:

- **PyQt5**: Creates the graphical user interface
- **NumPy**: Handles mathematical operations on image arrays
- **OpenCV**: Provides computer vision and image processing functions
- **PDF2Image**: Converts PDF pages to images
- **SciPy**: Additional scientific computing tools

The app processes images as NumPy arrays, which allows for fast mathematical operations. Most filters and transformations work on grayscale versions of color images, but the app preserves color information when possible.

## Tips for Best Results

- Use JPG or PNG files for best compatibility
- Large images will open in separate windows for easier viewing
- Try different kernel sizes with filters to see various effects
- Morphological operations work best on binary (black and white) images
- Save your work frequently when experimenting with different settings

---

Enjoy exploring the world of digital image processing!

P.S. The inspiration for the GUI was taken from this github repo below:
I forgot the name of that repo. Once I find it, I'll link it here. Also, if the person who owns that repo finds this repo, please comment your repo so I can provide the link :)