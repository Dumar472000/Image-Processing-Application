# ================================== All Libraries ==================================
# ===================================================================================

# ==== PyQt Modules ==== #
# PyQt Widgets
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
# PyQt Core
from PyQt5.QtCore import Qt
# PyQt Gui
from PyQt5.QtGui import QFont

# Image Processing Morphology Module
from image_processing.morphology import create_custom_structuring_element

# ===================================== Dialogs =====================================
# ===================================================================================

# PyQt5 Dialog for Filter Settings
class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔍 Filter Settings")
        self.setFixedSize(450, 280)
        
        # Modern dialog styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                border-radius: 15px;
            }
            QLabel {
                color: #ecf0f1;
                font-weight: bold;
                font-size: 14px;
            }
            QRadioButton {
                color: #ecf0f1;
                font-size: 12px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background: #34495e;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #3498db;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 2px solid #2980b9;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
                min-width: 85px;
                min-height: 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #2980b9, stop:1 #21618c);
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Filter Types
        filter_label = QLabel("🔍 Filter Types")
        filter_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(filter_label, 0, 0)
        
        self.filter_group = QButtonGroup()
        self.average_radio = QRadioButton("📊 Average Filter")
        self.median_radio = QRadioButton("🎯 Median Filter")
        self.laplace_radio = QRadioButton("🌊 Laplace Filter")
        
        self.average_radio.setChecked(True)  # Default selection
        
        self.filter_group.addButton(self.average_radio, 0)
        self.filter_group.addButton(self.median_radio, 1)
        self.filter_group.addButton(self.laplace_radio, 2)
        
        layout.addWidget(self.average_radio, 1, 0)
        layout.addWidget(self.median_radio, 2, 0)
        layout.addWidget(self.laplace_radio, 3, 0)
        
        # Kernel Size
        kernel_label = QLabel("⚙️ Kernel Size")
        kernel_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(kernel_label, 0, 1)
        
        self.kernel_group = QButtonGroup()
        self.kernel_3 = QRadioButton("3x3")
        self.kernel_5 = QRadioButton("5x5")
        self.kernel_7 = QRadioButton("7x7")
        self.kernel_9 = QRadioButton("9x9")
        self.kernel_11 = QRadioButton("11x11")
        
        self.kernel_3.setChecked(True)  # Default selection
        
        self.kernel_group.addButton(self.kernel_3, 3)
        self.kernel_group.addButton(self.kernel_5, 5)
        self.kernel_group.addButton(self.kernel_7, 7)
        self.kernel_group.addButton(self.kernel_9, 9)
        self.kernel_group.addButton(self.kernel_11, 11)
        
        layout.addWidget(self.kernel_3, 1, 1)
        layout.addWidget(self.kernel_5, 2, 1)
        layout.addWidget(self.kernel_7, 3, 1)
        layout.addWidget(self.kernel_9, 4, 1)
        layout.addWidget(self.kernel_11, 5, 1)
        
        # Buttons
        button_layout = QHBoxLayout()
        exit_btn = QPushButton("❌ Cancel")
        enter_btn = QPushButton("✅ Apply")
        
        exit_btn.clicked.connect(self.reject)
        enter_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(exit_btn)
        button_layout.addWidget(enter_btn)
        
        layout.addLayout(button_layout, 6, 0, 1, 2)
        
        self.setLayout(layout)
    
    def get_filter_type(self):
        if self.average_radio.isChecked():
            return "A"
        elif self.median_radio.isChecked():
            return "M"
        elif self.laplace_radio.isChecked():
            return "L"
        return "A"
    
    def get_kernel_size(self):
        if self.kernel_3.isChecked():
            return 3
        elif self.kernel_5.isChecked():
            return 5
        elif self.kernel_7.isChecked():
            return 7
        elif self.kernel_9.isChecked():
            return 9
        elif self.kernel_11.isChecked():
            return 11
        return 3


# PyQt5 Dialog for Thresholding Settings
class ThresholdDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚫ Thresholding Settings")
        self.setFixedSize(450, 250)
        
        # Modern dialog styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                border-radius: 15px;
            }
            QLabel {
                color: #ecf0f1;
                font-weight: bold;
                font-size: 14px;
            }
            QRadioButton {
                color: #ecf0f1;
                font-size: 12px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                background: #34495e;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #e74c3c;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
            QLineEdit {
                background: #34495e;
                color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QLineEdit:disabled {
                background: #2c3e50;
                color: #7f8c8d;
                border: 2px solid #7f8c8d;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: 2px solid #c0392b;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
                min-width: 85px;
                min-height: 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ec7063, stop:1 #e74c3c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #c0392b, stop:1 #a93226);
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Thresholding Types
        thresh_label = QLabel("⚫ Thresholding Methods")
        thresh_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(thresh_label, 0, 0, 1, 2)
        
        self.thresh_group = QButtonGroup()
        self.binary_otsu = QRadioButton("🎯 Binary-OTSU")
        self.simple_value = QRadioButton("📊 Simple-Value")
        self.adaptive_thresh = QRadioButton("🔄 Adaptive-Thresholding")
        
        self.binary_otsu.setChecked(True)  # Default selection
        
        self.thresh_group.addButton(self.binary_otsu, 0)
        self.thresh_group.addButton(self.simple_value, 1)
        self.thresh_group.addButton(self.adaptive_thresh, 2)
        
        layout.addWidget(self.binary_otsu, 1, 0)
        layout.addWidget(self.simple_value, 2, 0)
        layout.addWidget(self.adaptive_thresh, 3, 0)
        
        # Threshold Value
        value_label = QLabel("🔢 Threshold Value")
        value_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(value_label, 1, 1)
        
        self.threshold_entry = QLineEdit()
        self.threshold_entry.setPlaceholderText("Enter value (0-255)")
        self.threshold_entry.setEnabled(False)
        layout.addWidget(self.threshold_entry, 2, 1)
        
        # Connect radio buttons to enable/disable entry
        self.binary_otsu.toggled.connect(self.on_radio_changed)
        self.simple_value.toggled.connect(self.on_radio_changed)
        self.adaptive_thresh.toggled.connect(self.on_radio_changed)
        
        # Buttons
        button_layout = QHBoxLayout()
        exit_btn = QPushButton("❌ Cancel")
        enter_btn = QPushButton("✅ Apply")
        
        exit_btn.clicked.connect(self.reject)
        enter_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(exit_btn)
        button_layout.addWidget(enter_btn)
        
        layout.addLayout(button_layout, 4, 0, 1, 2)
        
        self.setLayout(layout)
    
    def on_radio_changed(self):
        if self.simple_value.isChecked():
            self.threshold_entry.setEnabled(True)
        else:
            self.threshold_entry.setEnabled(False)
            self.threshold_entry.clear()
    
    def get_threshold_type(self):
        if self.binary_otsu.isChecked():
            return "BO"
        elif self.simple_value.isChecked():
            return "SV"
        elif self.adaptive_thresh.isChecked():
            return "AT"
        return "BO"
    
    def get_threshold_value(self):
        try:
            return int(self.threshold_entry.text())
        except ValueError:
            return 124


# PyQt5 Dialog for Morphological Operations Settings
class MorphologicalDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔬 Morphological Operations")
        self.setFixedSize(500, 550)
        
        # Advanced modern styling for morphological dialog
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                border-radius: 15px;
            }
            QLabel {
                color: #ecf0f1;
                font-weight: bold;
                font-size: 13px;
            }
            QRadioButton {
                color: #ecf0f1;
                font-size: 11px;
                padding: 4px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #bdc3c7;
                border-radius: 9px;
                background: #34495e;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #f39c12;
                border-radius: 9px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f39c12, stop:1 #e67e22);
            }
            QLineEdit {
                background: #34495e;
                color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 4px;
                font-size: 11px;
                min-width: 60px;
            }
            QLineEdit:focus {
                border: 2px solid #f39c12;
            }
            QLineEdit:disabled {
                background: #2c3e50;
                color: #7f8c8d;
                border: 2px solid #7f8c8d;
            }
            QComboBox {
                background: #34495e;
                color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 4px;
                font-size: 11px;
                min-width: 80px;
            }
            QComboBox:focus {
                border: 2px solid #f39c12;
            }
            QComboBox:disabled {
                background: #2c3e50;
                color: #7f8c8d;
                border: 2px solid #7f8c8d;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #ecf0f1;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: #34495e;
                color: #ecf0f1;
                selection-background-color: #f39c12;
                selection-color: #2c3e50;
                border: 2px solid #f39c12;
                border-radius: 5px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: 2px solid #e67e22;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
                min-width: 85px;
                min-height: 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f7dc6f, stop:1 #f39c12);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #e67e22, stop:1 #d35400);
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Operation Types
        operation_label = QLabel("🔬 Morphological Operations")
        operation_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        layout.addWidget(operation_label, 0, 0, 1, 2)
        
        self.operation_group = QButtonGroup()
        self.erosion_radio = QRadioButton("🔻 Erosion")
        self.dilation_radio = QRadioButton("🔺 Dilation")
        self.opening_radio = QRadioButton("🔓 Opening")
        self.closing_radio = QRadioButton("🔒 Closing")
        
        self.erosion_radio.setChecked(True)  # Default selection
        
        self.operation_group.addButton(self.erosion_radio, 0)
        self.operation_group.addButton(self.dilation_radio, 1)
        self.operation_group.addButton(self.opening_radio, 2)
        self.operation_group.addButton(self.closing_radio, 3)
        
        layout.addWidget(self.erosion_radio, 1, 0)
        layout.addWidget(self.dilation_radio, 1, 1)
        layout.addWidget(self.opening_radio, 2, 0)
        layout.addWidget(self.closing_radio, 2, 1)
        
        # Structuring Element Shape
        shape_label = QLabel("🔧 Structuring Element Shape")
        shape_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        layout.addWidget(shape_label, 3, 0, 1, 2)
        
        self.shape_group = QButtonGroup()
        self.square_radio = QRadioButton("⬜ Square")
        self.circle_radio = QRadioButton("⭕ Circle")
        self.diamond_radio = QRadioButton("💎 Diamond")
        self.cross_radio = QRadioButton("➕ Cross")
        self.ellipse_radio = QRadioButton("🥚 Ellipse")
        self.t_radio = QRadioButton("🔛 T-Shape")
        self.slant_radio = QRadioButton("📐 Slant")
        self.polygon_radio = QRadioButton("🔷 Polygon")
        
        self.square_radio.setChecked(True)  # Default selection
        
        self.shape_group.addButton(self.square_radio, 0)
        self.shape_group.addButton(self.circle_radio, 1)
        self.shape_group.addButton(self.diamond_radio, 2)
        self.shape_group.addButton(self.cross_radio, 3)
        self.shape_group.addButton(self.ellipse_radio, 4)
        self.shape_group.addButton(self.t_radio, 5)
        self.shape_group.addButton(self.slant_radio, 6)
        self.shape_group.addButton(self.polygon_radio, 7)
        
        layout.addWidget(self.square_radio, 4, 0)
        layout.addWidget(self.circle_radio, 4, 1)
        layout.addWidget(self.diamond_radio, 5, 0)
        layout.addWidget(self.cross_radio, 5, 1)
        layout.addWidget(self.ellipse_radio, 6, 0)
        layout.addWidget(self.t_radio, 6, 1)
        layout.addWidget(self.slant_radio, 7, 0)
        layout.addWidget(self.polygon_radio, 7, 1)
        
        # Size Parameters
        size_label = QLabel("📏 Size Parameters")
        size_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        layout.addWidget(size_label, 8, 0, 1, 2)
        
        # Size/Radius entry
        size_label1 = QLabel("📐 Size/Radius:")
        self.size_entry = QLineEdit("3")
        self.size_entry.setPlaceholderText("3")
        layout.addWidget(size_label1, 9, 0)
        layout.addWidget(self.size_entry, 9, 1)
        
        # Width entry (for ellipse)
        width_label = QLabel("↔️ Width:")
        self.width_entry = QLineEdit("3")
        self.width_entry.setPlaceholderText("3")
        self.width_entry.setEnabled(False)
        layout.addWidget(width_label, 10, 0)
        layout.addWidget(self.width_entry, 10, 1)
        
        # Height entry (for ellipse)
        height_label = QLabel("↕️ Height:")
        self.height_entry = QLineEdit("3")
        self.height_entry.setPlaceholderText("3")
        self.height_entry.setEnabled(False)
        layout.addWidget(height_label, 11, 0)
        layout.addWidget(self.height_entry, 11, 1)
        
        # Direction entry (for slant)
        direction_label = QLabel("🔄 Direction:")
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["⬅️ Left", "➡️ Right"])
        self.direction_combo.setEnabled(False)
        layout.addWidget(direction_label, 12, 0)
        layout.addWidget(self.direction_combo, 12, 1)
        
        # Sides entry (for polygon)
        sides_label = QLabel("🔷 Sides:")
        self.sides_entry = QLineEdit("5")
        self.sides_entry.setPlaceholderText("5")
        self.sides_entry.setEnabled(False)
        layout.addWidget(sides_label, 13, 0)
        layout.addWidget(self.sides_entry, 13, 1)
        
        # Connect radio buttons to enable/disable entries
        self.ellipse_radio.toggled.connect(self.on_shape_changed)
        self.square_radio.toggled.connect(self.on_shape_changed)
        self.circle_radio.toggled.connect(self.on_shape_changed)
        self.diamond_radio.toggled.connect(self.on_shape_changed)
        self.cross_radio.toggled.connect(self.on_shape_changed)
        self.t_radio.toggled.connect(self.on_shape_changed)
        self.slant_radio.toggled.connect(self.on_shape_changed)
        self.polygon_radio.toggled.connect(self.on_shape_changed)
        
        # Buttons
        button_layout = QHBoxLayout()
        exit_btn = QPushButton("❌ Cancel")
        enter_btn = QPushButton("✅ Apply")
        
        exit_btn.clicked.connect(self.reject)
        enter_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(exit_btn)
        button_layout.addWidget(enter_btn)
        
        layout.addLayout(button_layout, 14, 0, 1, 2)
        
        self.setLayout(layout)
    
    def on_shape_changed(self):
        # Reset all to disabled first
        self.width_entry.setEnabled(False)
        self.height_entry.setEnabled(False)
        self.direction_combo.setEnabled(False)
        self.sides_entry.setEnabled(False)
        self.size_entry.setEnabled(True)  # Default enabled
        
        # Enable specific controls based on selection
        if self.ellipse_radio.isChecked():
            self.width_entry.setEnabled(True)
            self.height_entry.setEnabled(True)
            self.size_entry.setEnabled(False)
        elif self.slant_radio.isChecked():
            self.direction_combo.setEnabled(True)
        elif self.polygon_radio.isChecked():
            self.sides_entry.setEnabled(True)
    
    def get_operation_type(self):
        if self.erosion_radio.isChecked():
            return "erosion"
        elif self.dilation_radio.isChecked():
            return "dilation"
        elif self.opening_radio.isChecked():
            return "opening"
        elif self.closing_radio.isChecked():
            return "closing"
        return "erosion"
    
    def get_structuring_element(self):
        try:
            if self.ellipse_radio.isChecked():
                width = int(self.width_entry.text())
                height = int(self.height_entry.text())
                return create_custom_structuring_element('ellipse', width, height)
            elif self.slant_radio.isChecked():
                size = int(self.size_entry.text())
                direction_text = self.direction_combo.currentText()
                # Extract direction from emoji text
                direction = "left" if "Left" in direction_text else "right"
                return create_custom_structuring_element('slant', size, direction)
            elif self.polygon_radio.isChecked():
                size = int(self.size_entry.text())
                sides = int(self.sides_entry.text())
                return create_custom_structuring_element('polygon', size, sides)
            else:
                size = int(self.size_entry.text())
                if self.square_radio.isChecked():
                    return create_custom_structuring_element('square', size)
                elif self.circle_radio.isChecked():
                    return create_custom_structuring_element('circle', size)
                elif self.diamond_radio.isChecked():
                    return create_custom_structuring_element('diamond', size)
                elif self.cross_radio.isChecked():
                    return create_custom_structuring_element('cross', size)
                elif self.t_radio.isChecked():
                    return create_custom_structuring_element('t', size)
        except ValueError:
            # Return default 3x3 square if invalid input
            return create_custom_structuring_element('square', 3)
        
        return create_custom_structuring_element('square', 3)