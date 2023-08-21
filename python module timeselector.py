import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QDate, pyqtSignal, QTime

class TimeSelector(QWidget):
    # 创建一个自定义信号，用于在选择时间后发出
    time_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Time Selector')
        self.resize(350, 200)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 系统时间获取
        current_date = QDate.currentDate()
        current_time = QTime.currentTime()

        # Time Display
        self.time_display = QLabel('01-01 00:00', self)
        self.time_display.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.time_display)

        # Selectors
        selector_layout = QHBoxLayout()

        self.month_selector = QComboBox(self)
        self.day_selector = QComboBox(self)
        self.hour_selector = QComboBox(self)
        self.minute_selector = QComboBox(self)

        for i in range(1, 13):
            self.month_selector.addItem(f'{i:02d}')

        for i in range(24):
            self.hour_selector.addItem(f'{i:02d}')

        for i in range(60):
            self.minute_selector.addItem(f'{i:02d}')

        # 设置为当前时间
        self.month_selector.setCurrentIndex(current_date.month() - 1)
        self.update_day_selector()  # 先更新日数
        self.day_selector.setCurrentIndex(current_date.day() - 1)
        self.hour_selector.setCurrentIndex(current_time.hour())
        self.minute_selector.setCurrentIndex(current_time.minute())
        self.update_time_display()

        # 连接信号和槽
        self.month_selector.currentIndexChanged.connect(self.update_day_selector)
        self.month_selector.currentIndexChanged.connect(self.update_time_display)
        self.day_selector.currentIndexChanged.connect(self.update_time_display)
        self.hour_selector.currentIndexChanged.connect(self.update_time_display)
        self.minute_selector.currentIndexChanged.connect(self.update_time_display)

        selector_layout.addWidget(self.month_selector)
        selector_layout.addWidget(self.day_selector)
        selector_layout.addWidget(self.hour_selector)
        selector_layout.addWidget(self.minute_selector)
        main_layout.addLayout(selector_layout)

        self.confirm_btn = QPushButton('确定', self)
        self.confirm_btn.clicked.connect(self.emit_time_selected)
        main_layout.addWidget(self.confirm_btn)

    def update_day_selector(self):
        month = int(self.month_selector.currentText())
        year = QDate.currentDate().year()  # 获取当前年份

        days_in_month = QDate(year, month, 1).daysInMonth()  # 该方法会自动处理闰年

        # 保存当前的天数选择
        current_day = self.day_selector.currentText()
        self.day_selector.clear()

        for day in range(1, days_in_month + 1):
            self.day_selector.addItem(f'{day:02d}')

        # 如果先前选择的天数仍在新的天数范围内，则恢复选择
        index = self.day_selector.findText(current_day)
        if index != -1:
            self.day_selector.setCurrentIndex(index)

    def update_time_display(self):
        selected_date = f"{self.month_selector.currentText()}-{self.day_selector.currentText()} {self.hour_selector.currentText()}:{self.minute_selector.currentText()}"
        self.time_display.setText(selected_date)

    def emit_time_selected(self):
        self.time_selected.emit(self.time_display.text())
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimeSelector()
    ex.show()
    sys.exit(app.exec_())
