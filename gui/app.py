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

# ==== PyQt Modules ==== #
# PyQt Widgets
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
# PyQt Core
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
# PyQt Gui
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QFont

# ==== Image processing Modules ==== #
# Filtering
from image_processing.filtering import apply_averaging_filter
from image_processing.filtering import apply_median_filter
from image_processing.filtering import laplacian_filter
# Enhancing
from image_processing.enhancing import histEqualization
from image_processing.enhancing import ahe
# Thresholding
from image_processing.thresholding import adaptive_thresholding
from image_processing.thresholding import simple_thresholding
from image_processing.thresholding import Binary_OTSU
# Morphology
from image_processing.morphology import dilation
from image_processing.morphology import erosion
from image_processing.morphology import opening
from image_processing.morphology import closing
# Advanced
from image_processing.advanced import perform_color_clustering
from image_processing.advanced import laplacian_of_gaussian
from image_processing.advanced import segment_image

# Import utilities
from utils.utils import bgr_to_yuv
from utils.utils import yuv_to_bgr

# Import dialog classes
from .dialogs import MorphologicalDialog
from .dialogs import ThresholdDialog
from .dialogs import FilterDialog

# For Image Manipulation
from pdf2image import convert_from_path
import cv2

# Other Necessary Libraries
import numpy as np
import copy
import sys
import os

# ================================= Global Variables =================================
# ====================================================================================

# Global variables for image processing
original_image = None
changed_image = None
save_image = None
cap = None

# ================================= Main Application =================================
# ====================================================================================

# Main PyQt5 Application
class DigitalImageProcessingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupAnimationTimer()
        
    def initUI(self):
        self.setWindowTitle("Digital Image Processing Studio")
        self.setGeometry(100, 100, 900, 600)
        
        # Modern dark theme with gradients
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
            }
            QWidget {
                background: transparent;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout with spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        central_widget.setLayout(main_layout)
        
        # Title label
        title_label = QLabel("🖼️ Digital Image Processing Studio")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #ecf0f1;
                margin: 10px 0;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 15px;
                border: 2px solid #34495e;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Image display area with better styling
        image_container = QWidget()
        image_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 15px;
                border: 2px solid #3498db;
                padding: 20px;
            }
        """)
        image_layout = QHBoxLayout()
        image_layout.setSpacing(30)
        image_container.setLayout(image_layout)
        
        try:
            # Get the directory of this file and construct path to logo
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_dir, "assets", "fast_logo.png") # or any other logo of your choice
            fast_logo = QPixmap(logo_path)
            fast_logo = fast_logo.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except Exception as e:
            print(f"Could not load logo: {e}")
            # Create a placeholder if logo not found
            fast_logo = QPixmap(280, 280)
            fast_logo.fill(Qt.lightGray)
        
        # Panel A (left side) - Original Image
        panel_a_container = QWidget()
        panel_a_layout = QVBoxLayout()
        panel_a_layout.setAlignment(Qt.AlignCenter)
        
        original_label = QLabel("📁 Original Image")
        original_label.setAlignment(Qt.AlignCenter)
        original_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #3498db;
                margin-bottom: 10px;
            }
        """)
        
        self.panelA = QLabel()
        self.panelA.setPixmap(fast_logo)
        self.panelA.setFixedSize(280, 280)
        self.panelA.setAlignment(Qt.AlignCenter)
        self.panelA.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                border: 3px solid #3498db;
                border-radius: 15px;
                padding: 5px;
            }
        """)
        
        panel_a_layout.addWidget(original_label)
        panel_a_layout.addWidget(self.panelA)
        panel_a_container.setLayout(panel_a_layout)
        image_layout.addWidget(panel_a_container)
        
        # Panel B (right side) - Processed Image
        panel_b_container = QWidget()
        panel_b_layout = QVBoxLayout()
        panel_b_layout.setAlignment(Qt.AlignCenter)
        
        processed_label = QLabel("✨ Processed Image")
        processed_label.setAlignment(Qt.AlignCenter)
        processed_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #e74c3c;
                margin-bottom: 10px;
            }
        """)
        
        self.panelB = QLabel()
        self.panelB.setFixedSize(280, 280)
        self.panelB.setAlignment(Qt.AlignCenter)
        self.panelB.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                border: 3px solid #e74c3c;
                border-radius: 15px;
                padding: 5px;
            }
        """)
        
        panel_b_layout.addWidget(processed_label)
        panel_b_layout.addWidget(self.panelB)
        panel_b_container.setLayout(panel_b_layout)
        image_layout.addWidget(panel_b_container)
        
        main_layout.addWidget(image_container)
        
        # ComboBox for function selection
        combo_container = QWidget()
        combo_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 2px solid #95a5a6;
                padding: 10px;
            }
        """)
        combo_layout = QVBoxLayout()
        
        combo_label = QLabel("🔧 Select Processing Function")
        combo_label.setAlignment(Qt.AlignCenter)
        combo_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #f39c12;
                margin-bottom: 10px;
                border: none;
                background: transparent;
            }
        """)
        
        self.combo = QComboBox()
        self.combo.addItems([
            "🎯 Select a function",
            "🔍 A) Filters",
            "📊 B) Histogram-Equalization",
            "⚫ C) Thresholding",
            "☀️ D) Adjust Brightness",
            "🔆 E) Adjust Contrast by Multiplication",
            "⚡ F) Adjust Contrast by Power",
            "📏 G) Resize Image",
            "🔄 H) Rotate 90 degrees",
            "↔️ I) Horizontal Mirror",
            "↕️ J) Vertical Mirror",
            "🌊 K) Laplacian of Gaussian - LOG",
            "🎨 L) Clustering",
            "✂️ M) Image Segmentation",
            "🔬 N) Morphological Operations",
            "↩️ O) Revert All Changes"
        ])
        self.combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px 15px;
                min-height: 30px;
            }
            QComboBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8f9fa, stop:1 #dee2e6);
                border: 2px solid #2980b9;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #3498db;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background: #ecf0f1;
                color: #2c3e50;
                selection-background-color: #3498db;
                selection-color: white;
                border: 2px solid #3498db;
                border-radius: 5px;
            }
        """)
        
        combo_layout.addWidget(combo_label)
        combo_layout.addWidget(self.combo)
        combo_container.setLayout(combo_layout)
        main_layout.addWidget(combo_container)
        
        # Buttons container
        buttons_container = QWidget()
        buttons_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 2px solid #95a5a6;
                padding: 15px;
            }
        """)
        buttons_main_layout = QVBoxLayout()
        
        # First row of buttons
        button_layout1 = QHBoxLayout()
        button_layout1.setSpacing(15)
        
        self.btn_load = QPushButton("📁 Select Image")
        self.btn_update = QPushButton("⚡ Process Image")
        self.btn_save = QPushButton("💾 Save Image")
        self.btn_quit = QPushButton("🚪 Exit")
        
        # Modern button styling
        button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #2980b9;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5dade2, stop:1 #3498db);
                border: 2px solid #3498db;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2980b9, stop:1 #21618c);
                border: 2px solid #21618c;
            }
        """
        
        save_button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #27ae60, stop:1 #229954);
                border: 2px solid #229954;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #58d68d, stop:1 #27ae60);
                border: 2px solid #27ae60;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #229954, stop:1 #1e8449);
                border: 2px solid #1e8449;
            }
        """
        
        quit_button_style = """
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e74c3c, stop:1 #c0392b);
                border: 2px solid #c0392b;
                border-radius: 12px;
                padding: 12px 20px;
                min-height: 20px;
                min-width: 120px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ec7063, stop:1 #e74c3c);
                border: 2px solid #e74c3c;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c0392b, stop:1 #a93226);
                border: 2px solid #a93226;
            }
        """
        
        self.btn_load.setStyleSheet(button_style)
        self.btn_update.setStyleSheet(button_style)
        self.btn_save.setStyleSheet(save_button_style)
        self.btn_quit.setStyleSheet(quit_button_style)
        
        # Connect button signals
        self.btn_load.clicked.connect(self.select_image)
        self.btn_update.clicked.connect(self.perform_function)
        self.btn_save.clicked.connect(self.save_image_function)
        self.btn_quit.clicked.connect(self.close)
        
        button_layout1.addWidget(self.btn_load)
        button_layout1.addWidget(self.btn_update)
        button_layout1.addWidget(self.btn_save)
        button_layout1.addWidget(self.btn_quit)
        
        # Second row of buttons (for video navigation)
        button_layout2 = QHBoxLayout()
        button_layout2.setSpacing(15)
        
        # Spacer
        button_layout2.addStretch()
        
        self.btn_prev = QPushButton("⏮️ Previous")
        self.btn_next = QPushButton("⏭️ Next")
        
        nav_button_style = """
            QPushButton {
                font-size: 12px;
                font-weight: bold;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f39c12, stop:1 #e67e22);
                border: 2px solid #e67e22;
                border-radius: 10px;
                padding: 8px 16px;
                min-height: 15px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f7dc6f, stop:1 #f39c12);
                border: 2px solid #f39c12;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e67e22, stop:1 #d35400);
                border: 2px solid #d35400;
            }
        """
        
        self.btn_prev.setStyleSheet(nav_button_style)
        self.btn_next.setStyleSheet(nav_button_style)
        
        self.btn_prev.clicked.connect(self.prev_frame)
        self.btn_next.clicked.connect(self.next_frame)
        
        button_layout2.addWidget(self.btn_prev)
        button_layout2.addWidget(self.btn_next)
        button_layout2.addStretch()
        
        # Add layouts to buttons container
        buttons_main_layout.addLayout(button_layout1)
        buttons_main_layout.addLayout(button_layout2)
        buttons_container.setLayout(buttons_main_layout)
        main_layout.addWidget(buttons_container)
        
        # Additional windows
        self.before_window = None
        self.after_window = None
        self.panelC = None
        self.panelD = None
        
        # Animation variables
        self.angle = np.pi / 4
        self.speed = 0.1
        
    def setupAnimationTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_panelB)
        self.timer.start(100)  # Update every 100ms
        
    def update_panelB(self):
        x = np.linspace(0, 1, 280)
        y = np.linspace(0, 1, 280)
        X, Y = np.meshgrid(x, y)
        
        # Generate more sophisticated animated patterns
        time_factor = self.angle * 0.5
        
        # Create dynamic wave patterns
        red_channel = (np.sin(np.pi * (X * np.cos(self.angle) + Y * np.sin(self.angle)) - time_factor) + 1) * 127.5
        green_channel = (np.sin(np.pi * (X * np.cos(self.angle + np.pi/3) + Y * np.sin(self.angle + np.pi/3)) - time_factor) + 1) * 127.5
        blue_channel = (np.sin(np.pi * (X * np.cos(self.angle + 2*np.pi/3) + Y * np.sin(self.angle + 2*np.pi/3)) - time_factor) + 1) * 127.5
        
        # Add circular wave effect
        center_x, center_y = 140, 140
        distance = np.sqrt((X * 280 - center_x)**2 + (Y * 280 - center_y)**2)
        wave_effect = np.sin(distance * 0.1 - time_factor * 2) * 30
        
        red_channel = np.clip(red_channel + wave_effect, 0, 255)
        green_channel = np.clip(green_channel + wave_effect * 0.8, 0, 255)
        blue_channel = np.clip(blue_channel + wave_effect * 0.6, 0, 255)
        
        # Combine RGB channels
        image_array = np.stack((red_channel, green_channel, blue_channel), axis=-1).astype(np.uint8)
        
        # Ensure the image array is contiguous in memory
        image_array = np.ascontiguousarray(image_array)
        
        # Convert to QPixmap
        height, width, channel = image_array.shape
        bytes_per_line = 3 * width
        q_image = QImage(image_array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_pixmap = QPixmap.fromImage(q_image)
        
        self.panelB.setPixmap(q_pixmap)
        self.angle += 0.03
        
    def select_image(self):
        global original_image, changed_image, save_image, cap
        
        save_image = None
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Image or Video", 
            "", 
            "All Files (*);;Images (*.png *.jpg *.jpeg);;PDF (*.pdf);;Videos (*.mp4 *.avi *.mov)"
        )
        
        if file_path:
            if cap:
                cap.release()
            
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                original_image = cv2.imread(file_path)
                original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
                changed_image = original_image.copy()
                self.display_image(changed_image)
            elif file_path.lower().endswith('.pdf'):
                try:
                    images = convert_from_path(file_path)
                    if images:
                        original_image = np.array(images[0])
                        changed_image = original_image.copy()
                        self.display_image(changed_image)
                    else:
                        QMessageBox.warning(self, "Error", "No images found in the PDF.")
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Error loading PDF: {str(e)}")
            else:
                cap = cv2.VideoCapture(file_path)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        changed_image = original_image.copy()
                        self.display_image(changed_image)
                else:
                    QMessageBox.warning(self, "Error", "Error opening file.")
    
    def display_image(self, image, is_processed=False):
        # Convert numpy array to QPixmap
        height, width = image.shape[:2]
        
        # Ensure the image array is contiguous in memory
        image = np.ascontiguousarray(image)
        
        if len(image.shape) == 3:
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        q_pixmap = QPixmap.fromImage(q_image)
        q_pixmap = q_pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        if original_image.shape[0] > 280 or original_image.shape[1] > 280:
            # Show additional windows for large images
            if is_processed:
                # If this is a processed image, show the before/after windows
                self.show_additional_windows(image)
            else:
                # If this is just loading an image, hide the windows
                if self.before_window:
                    self.before_window.hide()
                if self.after_window:
                    self.after_window.hide()
        else:
            self.panelA.setPixmap(q_pixmap)
            if self.before_window:
                self.before_window.hide()
            if self.after_window:
                self.after_window.hide()
    
    def show_additional_windows(self, processed_image):
        # Create before and after windows if they don't exist
        if not self.before_window:
            self.before_window = QWidget()
            self.before_window.setWindowTitle("📁 Before Image Processing")
            self.before_window.setFixedSize(450, 450)
            self.before_window.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #2c3e50, stop:1 #34495e);
                    color: #ecf0f1;
                    border-radius: 10px;
                }
                QLabel {
                    border: 3px solid #3498db;
                    border-radius: 10px;
                    background: #2c3e50;
                }
            """)
            layout = QVBoxLayout()
            layout.setContentsMargins(15, 15, 15, 15)
            self.panelC = QLabel()
            self.panelC.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.panelC)
            self.before_window.setLayout(layout)
        
        if not self.after_window:
            self.after_window = QWidget()
            self.after_window.setWindowTitle("✨ After Image Processing")
            self.after_window.setFixedSize(450, 450)
            self.after_window.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                        stop:0 #2c3e50, stop:1 #34495e);
                    color: #ecf0f1;
                    border-radius: 10px;
                }
                QLabel {
                    border: 3px solid #e74c3c;
                    border-radius: 10px;
                    background: #2c3e50;
                }
            """)
            layout = QVBoxLayout()
            layout.setContentsMargins(15, 15, 15, 15)
            self.panelD = QLabel()
            self.panelD.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.panelD)
            self.after_window.setLayout(layout)
        
        # Display original image in "Before" window (panelC)
        self.update_window_image(original_image, self.panelC)
        
        # Display processed image in "After" window (panelD)
        self.update_window_image(processed_image, self.panelD)
        
        # Show windows
        self.before_window.show()
        self.after_window.show()
    
    def update_window_image(self, image, panel):
        """Helper method to update image in a specific panel"""
        if image is None or panel is None:
            return
            
        # Convert and display image
        height, width = image.shape[:2]
        
        # Ensure the image array is contiguous in memory
        image = np.ascontiguousarray(image)
        
        if len(image.shape) == 3:
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        else:
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        
        q_pixmap = QPixmap.fromImage(q_image)
        q_pixmap = q_pixmap.scaled(420, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        panel.setPixmap(q_pixmap)
    
    def update_after_window(self, processed_image):
        """Update only the 'After' window with processed image"""
        if hasattr(self, 'panelD') and self.panelD and self.after_window:
            self.update_window_image(processed_image, self.panelD)
    
    def perform_function(self):
        global original_image, changed_image, save_image
        
        if original_image is None:
            QMessageBox.warning(self, "No Image Error", "Please select an image to perform function on.")
            return
        
        selection = self.combo.currentText()
        if not selection or "Select a function" in selection:
            QMessageBox.warning(self, "No Function Error", "Please select function to perform first.")
            return
        
        # Extract the function letter from the selection text
        if "A)" in selection:
            selection_char = 'A'
        elif "B)" in selection:
            selection_char = 'B'
        elif "C)" in selection:
            selection_char = 'C'
        elif "D)" in selection:
            selection_char = 'D'
        elif "E)" in selection:
            selection_char = 'E'
        elif "F)" in selection:
            selection_char = 'F'
        elif "G)" in selection:
            selection_char = 'G'
        elif "H)" in selection:
            selection_char = 'H'
        elif "I)" in selection:
            selection_char = 'I'
        elif "J)" in selection:
            selection_char = 'J'
        elif "K)" in selection:
            selection_char = 'K'
        elif "L)" in selection:
            selection_char = 'L'
        elif "M)" in selection:
            selection_char = 'M'
        elif "N)" in selection:
            selection_char = 'N'
        elif "O)" in selection:
            selection_char = 'O'
        else:
            QMessageBox.warning(self, "Invalid Selection", "Please select a valid function.")
            return
        
        if selection_char == 'A':  # Filters
            dialog = FilterDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                filter_type = dialog.get_filter_type()
                kernel_size = dialog.get_kernel_size()
                
                if filter_type == 'A':
                    changed_image = apply_averaging_filter(changed_image, kernel_size)
                elif filter_type == 'M':
                    changed_image = apply_median_filter(changed_image, kernel_size)
                else:
                    changed_image = laplacian_filter(changed_image, kernel_size)
                
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'B':  # Histogram Equalization
            from PyQt5.QtWidgets import QInputDialog
            methods = ["Global", "Adaptive"]
            method, ok = QInputDialog.getItem(self, "Histogram Equalization", "Select method:", methods, 0, False)
            
            if ok:
                if method.lower() == 'global':
                    # Check if image is grayscale or color
                    if len(changed_image.shape) == 2:
                        # Grayscale image - apply histogram equalization directly
                        changed_image = histEqualization(changed_image)
                    else:
                        # Color image - convert to YUV, equalize Y channel, convert back
                        changed_image = bgr_to_yuv(changed_image)
                        changed_image[..., 0] = histEqualization(changed_image[..., 0])
                        changed_image = yuv_to_bgr(changed_image)
                elif method.lower() == 'adaptive':
                    # Check if image is grayscale or color
                    if len(changed_image.shape) == 2:
                        # Grayscale image - apply adaptive histogram equalization directly
                        changed_image = ahe(changed_image)
                    else:
                        # Color image - use HSV color space
                        hsv = cv2.cvtColor(changed_image, cv2.COLOR_RGB2HSV)
                        h, s, v = cv2.split(hsv)
                        ahe_v = ahe(v)
                        merged_ahe = cv2.merge((h, s, ahe_v))
                        changed_image = cv2.cvtColor(merged_ahe, cv2.COLOR_HSV2RGB)
                
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'C':  # Thresholding
            dialog = ThresholdDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                threshold_type = dialog.get_threshold_type()
                threshold_value = dialog.get_threshold_value()
                
                if threshold_type == 'BO':
                    changed_image = Binary_OTSU(changed_image)
                elif threshold_type == 'AT':
                    changed_image = adaptive_thresholding(changed_image, 3, 2)
                elif threshold_type == 'SV':
                    if not (0 <= threshold_value <= 255):
                        QMessageBox.warning(self, "Invalid Threshold", "Please enter a value between 0-255.")
                        return
                    changed_image = simple_thresholding(changed_image, threshold_value)
                
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'D':  # Brightness
            from PyQt5.QtWidgets import QInputDialog
            value, ok = QInputDialog.getInt(self, "Brightness", "Enter brightness value to add/subtract:", 0, -255, 255)
            
            if ok:
                changed_image = np.clip(changed_image.astype(np.float32) + value, 0, 255).astype(np.uint8)
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'E':  # Contrast (multiplication)
            from PyQt5.QtWidgets import QInputDialog
            value, ok = QInputDialog.getDouble(self, "Contrast", "Enter contrast multiplier:", 1.0, 0.1, 10.0, 2)
            
            if ok:
                changed_image = np.clip(changed_image.astype(np.float32) * value, 0, 255).astype(np.uint8)
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'F':  # Contrast (power)
            from PyQt5.QtWidgets import QInputDialog
            power, ok = QInputDialog.getDouble(self, "Contrast Power", "Enter power value:", 1.0, 0.1, 5.0, 2)
            
            if ok:
                changed_image = np.array(255 * (changed_image / 255) ** power, dtype='uint8')
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'G':  # Resize
            from PyQt5.QtWidgets import QInputDialog
            width, ok1 = QInputDialog.getInt(self, "Resize", f"Enter width (current: {original_image.shape[1]}):", original_image.shape[1], 1, 5000)
            if ok1:
                height, ok2 = QInputDialog.getInt(self, "Resize", f"Enter height (current: {original_image.shape[0]}):", original_image.shape[0], 1, 5000)
                if ok2:
                    changed_image = cv2.resize(changed_image, (width, height), interpolation=cv2.INTER_AREA)
                    save_image = copy.deepcopy(changed_image)
                    self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'H':  # Rotate
            changed_image = np.transpose(changed_image, (1, 0, 2))[:, ::-1]
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'I':  # Horizontal flip
            changed_image = np.flip(changed_image, axis=1)
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'J':  # Vertical flip
            changed_image = np.flipud(changed_image)
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'K':  # Laplacian of Gaussian
            changed_image = laplacian_of_gaussian(changed_image, 3)
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'L':  # Clustering
            changed_image = perform_color_clustering(changed_image, num_clusters=2)
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'M':  # Segmentation
            changed_image = segment_image(changed_image)
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'N':  # Morphological Operations
            dialog = MorphologicalDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                operation_type = dialog.get_operation_type()
                structuring_element = dialog.get_structuring_element()
                
                if operation_type == 'erosion':
                    changed_image = erosion(changed_image, structuring_element)
                elif operation_type == 'dilation':
                    changed_image = dilation(changed_image, structuring_element)
                elif operation_type == 'opening':
                    changed_image = opening(changed_image, structuring_element)
                elif operation_type == 'closing':
                    changed_image = closing(changed_image, structuring_element)
                
                save_image = copy.deepcopy(changed_image)
                self.display_image(changed_image, is_processed=True)
        
        elif selection_char == 'O':  # Revert
            changed_image = original_image.copy()
            save_image = copy.deepcopy(changed_image)
            self.display_image(changed_image, is_processed=True)
    
    def save_image_function(self):
        global save_image
        
        if save_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Image",
                "",
                "JPEG Files (*.jpg);;PNG Files (*.png);;All Files (*)"
            )
            if file_path:
                # Handle both grayscale and color images
                if len(save_image.shape) == 3:
                    # Convert RGB back to BGR for OpenCV
                    save_image_bgr = cv2.cvtColor(save_image, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(file_path, save_image_bgr)
                else:
                    # Grayscale image - save directly
                    cv2.imwrite(file_path, save_image)
        else:
            QMessageBox.warning(self, "No Modified Image", "Please select an image and perform operation before saving.")
    
    def next_frame(self):
        global cap, original_image, changed_image
        
        if cap is not None:
            ret, frame = cap.read()
            if ret:
                original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                changed_image = original_image.copy()
                self.display_image(changed_image, is_processed=False)
    
    def prev_frame(self):
        global cap, original_image, changed_image
        
        if cap is not None:
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if pos > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos - 2)
                ret, frame = cap.read() 
                if ret:
                    original_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    changed_image = original_image.copy()
                    self.display_image(changed_image, is_processed=False)
