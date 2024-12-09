import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QCalendarWidget
from PyQt5.QtCore import Qt, QDate, QPropertyAnimation, QRect
from PyQt5.QtGui import QPalette, QColor, QFont
from datetime import date

class AgeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Age Calculator")
        self.setStyleSheet("background-color: #f0f8ff;")
        self.setFixedSize(600, 500)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel("Age Calculator")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Calendar
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setStyleSheet("""
            QCalendarWidget QToolButton {
                color: #2c3e50;
                font-size: 14px;
                icon-size: 20px;
            }
            QCalendarWidget QMenu {
                background-color: white;
            }
            QCalendarWidget QSpinBox {
                font-size: 14px;
            }
        """)
        palette = self.calendar.palette()
        palette.setColor(QPalette.Highlight, QColor("#3498db"))
        self.calendar.setPalette(palette)
        layout.addWidget(self.calendar)
        
        # Result Label
        self.result_label = QLabel("Select your birthdate")
        self.result_label.setFont(QFont('Arial', 16))
        self.result_label.setStyleSheet("color: #2c3e50; padding: 20px;")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Connect calendar signal
        self.calendar.clicked.connect(self.calculate_age)
        
        # Animation setup
        self.animation = QPropertyAnimation(self.result_label, b"geometry")
        self.animation.setDuration(500)
        
    def calculate_age(self):
        birth_date = self.calendar.selectedDate().toPyDate()
        today = date.today()
        
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day
        
        if days < 0:
            months -= 1
            days += 30  # Assuming 30 days per month for simplicity
            
        if months < 0:
            years -= 1
            months += 12
            
        # Animate result
        self.animate_result()
        
        # Update result text
        result_text = f"You are {years} years, {months} months, and {days} days old"
        self.result_label.setText(result_text)
        
    def animate_result(self):
        # Create bounce animation
        current_geometry = self.result_label.geometry()
        
        # Move up
        self.animation.setStartValue(current_geometry)
        end_geometry = QRect(current_geometry.x(), current_geometry.y() - 20,
                           current_geometry.width(), current_geometry.height())
        self.animation.setEndValue(end_geometry)
        self.animation.start()
        
        # Move back down
        self.animation.finished.connect(lambda: self.bounce_back(current_geometry))
        
    def bounce_back(self, original_geometry):
        self.animation.setStartValue(self.animation.endValue())
        self.animation.setEndValue(original_geometry)
        self.animation.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = AgeCalculator()
    calculator.show()
    sys.exit(app.exec_())
