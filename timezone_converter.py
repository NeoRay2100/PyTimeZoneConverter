import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QListWidget
from PyQt5.QtCore import Qt, QDateTime, QTimeZone
import pytz

class TimezoneConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("时区转换器")
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 时区选择器
        selector_layout = QHBoxLayout()
        self.from_timezone = QComboBox()
        self.to_timezone = QComboBox()
        selector_layout.addWidget(QLabel("从时区："))
        selector_layout.addWidget(self.from_timezone)
        selector_layout.addWidget(QLabel("到时区："))
        selector_layout.addWidget(self.to_timezone)
        main_layout.addLayout(selector_layout)

        # 时间显示
        time_layout = QHBoxLayout()
        self.from_time_list = QListWidget()
        self.to_time_list = QListWidget()
        time_layout.addWidget(self.from_time_list)
        time_layout.addWidget(self.to_time_list)
        main_layout.addLayout(time_layout)

        self.populate_timezones()
        self.from_timezone.setCurrentText("UTC")
        self.to_timezone.setCurrentText("Asia/Shanghai")

        self.from_timezone.currentTextChanged.connect(self.update_time_lists)
        self.to_timezone.currentTextChanged.connect(self.update_time_lists)

        self.update_time_lists()

    def populate_timezones(self):
        timezones = pytz.all_timezones
        self.from_timezone.addItems(timezones)
        self.to_timezone.addItems(timezones)

    def update_time_lists(self):
        self.from_time_list.clear()
        self.to_time_list.clear()

        from_tz = pytz.timezone(self.from_timezone.currentText())
        to_tz = pytz.timezone(self.to_timezone.currentText())

        for hour in range(24):
            from_time = QDateTime.currentDateTime().toPyDateTime().replace(hour=hour, minute=0, second=0, microsecond=0)
            from_time = from_tz.localize(from_time)
            to_time = from_time.astimezone(to_tz)

            self.from_time_list.addItem(from_time.strftime("%H:%M"))
            self.to_time_list.addItem(to_time.strftime("%H:%M"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimezoneConverter()
    window.show()
    sys.exit(app.exec_())
