from PyQt6 import QtCore, QtGui, QtWidgets
from VisualizationSort import *
import requests, json, time, pandas as pd
from SortingAlgorithm import selection_sort, quick_sort

class Input:
    def validate_data(self, temperature, humidity):
        """Kiểm tra tính hợp lệ của dữ liệu."""
        try:
            temp = float(temperature.split()[0])  # Tách số từ chuỗi "XX.XX °C"
            if temp < -100 or temp > 100:
                return False, "Nhiệt độ phải nằm trong khoảng từ -100°C đến 100°C."
        except (ValueError, IndexError):
            return False, "Nhiệt độ không hợp lệ."

        try:
            hum = float(humidity.split()[0])  # Tách số từ chuỗi "XX.XX %"
            if hum < 0 or hum > 100:
                return False, "Độ ẩm phải nằm trong khoảng từ 0% đến 100%."
        except (ValueError, IndexError):
            return False, "Độ ẩm không hợp lệ."

        return True, ""

    def input_from_keyboard(self, city, temperature, humidity, wind_speed):
        """Nhập dữ liệu từ giao diện."""
        if not city:
            QtWidgets.QMessageBox.warning(None, "Error", "Vui lòng nhập tên thành phố!")
            return None

        try:
            temperature = float(temperature)
            if temperature < -100 or temperature > 100:
                raise ValueError("Nhiệt độ phải nằm trong khoảng từ -100°C đến 100°C.")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Lỗi nhiệt độ: {str(e)}")
            return None

        try:
            humidity = float(humidity)
            if humidity < 0 or humidity > 100:
                raise ValueError("Độ ẩm phải nằm trong khoảng từ 0% đến 100%.")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Lỗi độ ẩm: {str(e)}")
            return None

        try:
            wind_speed = float(wind_speed)
            if wind_speed < 0:
                raise ValueError("Tốc độ gió không thể âm!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Lỗi tốc độ gió: {str(e)}")
            return None

        return {
            "city": city,
            "temperature": f"{temperature} °C",
            "wind_speed": f"{wind_speed} m/s",
            "humidity": f"{humidity} %"
        }

    def input_from_file(self, file_path):
        """Đọc dữ liệu từ file CSV."""
        try:
            # Đọc file CSV
            df = pd.read_csv(file_path)
            
            # Kiểm tra các cột bắt buộc
            required_columns = ['city', 'temperature', 'wind_speed', 'humidity']
            if not all(col in df.columns for col in required_columns):
                QtWidgets.QMessageBox.warning(None, "Error", "File CSV không có đủ các cột cần thiết!")
                return None
                
            valid_data = []
            for _, row in df.iterrows():
                try:
                    temp = float(row['temperature'])
                    humidity = float(row['humidity'])
                    wind_speed = float(row['wind_speed'])
                    
                    # Kiểm tra giới hạn
                    if temp < -100 or temp > 100:
                        continue
                    if humidity < 0 or humidity > 100:
                        continue
                    if wind_speed < 0:
                        continue
                        
                    valid_data.append({
                        'city': row['city'],
                        'temperature': f"{temp} °C",
                        'wind_speed': f"{wind_speed} m/s",
                        'humidity': f"{humidity} %"
                    })
                    
                except (ValueError, TypeError):
                    continue
                    
            if not valid_data:
                QtWidgets.QMessageBox.warning(None, "Warning", "Không có dữ liệu hợp lệ trong file!")
                return None
                
            return valid_data
                    
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(None, "Error", "Không tìm thấy file!")
            return None
        except pd.errors.EmptyDataError:
            QtWidgets.QMessageBox.warning(None, "Error", "File CSV trống!")
            return None
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Lỗi khi đọc file: {str(e)}")
            return None

    def input_from_api(self, city):
        """Gọi dữ liệu thời tiết từ API."""
        API_KEY = "5fa789c022def2ca3417c45d533465e5"
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
        try:
            url = BASE_URL + f"appid={API_KEY}&q={city}"
            response = requests.get(url).json()

            if response.get("cod") != 200:
                QtWidgets.QMessageBox.warning(None, "Error", f"Không tìm thấy thành phố: {city}")
                return None

            temp_kelvin = response["main"]["temp"]
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]
            temp_celsius = temp_kelvin - 273.15

            if temp_celsius < -100 or temp_celsius > 100:
                QtWidgets.QMessageBox.warning(None, "Error", "Nhiệt độ từ API vượt quá giới hạn cho phép (-100°C đến 100°C).")
                return None

            if humidity < 0 or humidity > 100:
                QtWidgets.QMessageBox.warning(None, "Error", "Độ ẩm từ API vượt quá giới hạn cho phép (0% đến 100%).")
                return None

            return {
                "city": city,
                "temperature": f"{temp_celsius:.2f} °C",
                "wind_speed": f"{wind_speed} m/s",
                "humidity": f"{humidity} %"
            }
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã xảy ra lỗi: {str(e)}")
            return None

class Ui_MainWindow(Input):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 630)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonDeleteRow = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteRow.setGeometry(QtCore.QRect(10, 550, 131, 28))
        self.buttonDeleteRow.setObjectName("buttonDeleteRow")
        self.buttonDeleteAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteAll.setGeometry(QtCore.QRect(150, 550, 111, 28))
        self.buttonDeleteAll.setObjectName("buttonDeleteAll")
        self.buttonVisualizationSort = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonVisualizationSort.setGeometry(QtCore.QRect(265, 550, 93, 28))
        self.buttonVisualizationSort.setObjectName("buttonVisualizationSort")

        self.buttonSortAscending = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonSortAscending.setGeometry(QtCore.QRect(360, 550, 130, 28))
        self.buttonSortAscending.setObjectName("buttonSortAscending")

        self.buttonSortDescending = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonSortDescending.setGeometry(QtCore.QRect(495, 550, 130, 28))
        self.buttonSortDescending.setObjectName("buttonSortDescending")

        self.cbTieuChi = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbTieuChi.setGeometry(QtCore.QRect(20, 310, 101, 22))
        self.cbTieuChi.setObjectName("cbTieuChi")
        self.cbTieuChi.addItem("")
        self.cbTieuChi.addItem("")
        self.cbTieuChi.addItem("")
        self.cbLoaiSapXep = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbLoaiSapXep.setGeometry(QtCore.QRect(20, 360, 101, 22))
        self.cbLoaiSapXep.setObjectName("cbLoaiSapXep")
        self.cbLoaiSapXep.addItem("")
        self.cbLoaiSapXep.addItem("")

        self.cbDataInput = QtWidgets.QComboBox(parent=self.centralwidget)
        self.cbDataInput.setGeometry(QtCore.QRect(20, 50, 200, 22))
        self.cbDataInput.setObjectName("cbDataInput")
        self.cbDataInput.addItem("Lấy dữ liệu trực tiếp")
        self.cbDataInput.addItem("Lấy dữ liệu từ file có sẵn")
        self.cbDataInput.addItem("Nhập tay")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 100, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 140, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 180, 55, 16))
        self.label_3.setObjectName("label_3")
        self.editNhietDo = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editNhietDo.setGeometry(QtCore.QRect(250, 100, 113, 22))
        self.editNhietDo.setReadOnly(True)
        self.editNhietDo.setObjectName("editNhietDo")
        self.editTocDoGio = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editTocDoGio.setGeometry(QtCore.QRect(250, 140, 113, 22))
        self.editTocDoGio.setReadOnly(True)
        self.editTocDoGio.setObjectName("editTocDoGio")
        self.editDoAm = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editDoAm.setGeometry(QtCore.QRect(250, 180, 113, 22))
        self.editDoAm.setReadOnly(True)
        self.editDoAm.setObjectName("editDoAm")
        self.inputThanhPho = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.inputThanhPho.setGeometry(QtCore.QRect(250, 50, 113, 22))
        self.inputThanhPho.setObjectName("inputThanhPho")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(400, 50, 113, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(235, 230, 141, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(140, 300, 470, 200))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Thành Phố", "Nhiệt Độ (°C)", "Tốc Độ Gió (m/s)", "Độ Ẩm (%)"])
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.cbDataInput.currentTextChanged.connect(self.on_data_input_change)
        self.pushButton.clicked.connect(self.fetch_weather_data)
        self.pushButton_2.clicked.connect(self.show_data_on_table)
        self.buttonDeleteRow.clicked.connect(self.delete_selected_row)
        self.buttonDeleteAll.clicked.connect(self.delete_all_rows)
        self.buttonVisualizationSort.clicked.connect(self.visualization_sort_window)
        self.buttonSortAscending.clicked.connect(self.sort_table_ascending)
        self.buttonSortDescending.clicked.connect(self.sort_table_descending)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonDeleteRow.setText(_translate("MainWindow", "Xóa hàng đang chọn"))
        self.buttonDeleteAll.setText(_translate("MainWindow", "Xóa tất cả hàng"))
        self.buttonVisualizationSort.setText(_translate("MainWindow", "Trực quan"))
        self.cbTieuChi.setItemText(0, _translate("MainWindow", "Nhiệt độ"))
        self.cbTieuChi.setItemText(1, _translate("MainWindow", "Tốc độ gió"))
        self.cbTieuChi.setItemText(2, _translate("MainWindow", "Độ ẩm"))
        self.label.setText(_translate("MainWindow", "Nhiệt độ"))
        self.label_2.setText(_translate("MainWindow", "Tốc độ gió"))
        self.label_3.setText(_translate("MainWindow", "Độ ẩm"))
        self.cbLoaiSapXep.setItemText(0, _translate("MainWindow", "Selection Sort"))
        self.cbLoaiSapXep.setItemText(1, _translate("MainWindow", "Quick Sort"))
        self.pushButton.setText(_translate("MainWindow", "Nhập Thành Phố"))
        self.pushButton_2.setText(_translate("MainWindow", "Hiện Kết Quả Lên Bảng"))
        self.buttonSortAscending.setText(_translate("MainWindow", "Sắp xếp tăng dần"))
        self.buttonSortDescending.setText(_translate("MainWindow", "Sắp xếp giảm dần"))

    def on_data_input_change(self, text):
        if text == "Nhập tay":
            self.editNhietDo.setReadOnly(False)
            self.editTocDoGio.setReadOnly(False)
            self.editDoAm.setReadOnly(False)
        else:
            self.editNhietDo.setReadOnly(True)
            self.editTocDoGio.setReadOnly(True)
            self.editDoAm.setReadOnly(True)

    def fetch_weather_data(self):
        """Lấy dữ liệu thời tiết từ nguồn được chọn."""
        if self.cbDataInput.currentText() == "Lấy dữ liệu trực tiếp":
            city = self.inputThanhPho.text()
            if not city:
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập tên thành phố!")
                return
            data = self.input_from_api(city)
            if data:
                self.editNhietDo.setText(data["temperature"])
                self.editTocDoGio.setText(data["wind_speed"])
                self.editDoAm.setText(data["humidity"])
                
        elif self.cbDataInput.currentText() == "Nhập tay":
            city = self.inputThanhPho.text()
            temperature = self.editNhietDo.text()
            wind_speed = self.editTocDoGio.text()
            humidity = self.editDoAm.text()
            
            if not all([city, temperature, wind_speed, humidity]):
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập đầy đủ thông tin!")
                return
                
            data = self.input_from_keyboard(city, temperature, humidity, wind_speed)
            if data:
                self.editNhietDo.setText(data["temperature"])
                self.editTocDoGio.setText(data["wind_speed"])
                self.editDoAm.setText(data["humidity"])

        elif self.cbDataInput.currentText() == "Lấy dữ liệu từ file có sẵn":
            file_path = "weather_data_20241229_0114.csv"  
            data_list = self.input_from_file(file_path)
            if data_list:
                # Xóa dữ liệu cũ trong bảng
                self.tableWidget.setRowCount(0)
                
                # Thêm từng bản ghi vào bảng
                for data in data_list:
                    self.add_row_to_table(
                        data["city"],
                        data["temperature"],
                        data["wind_speed"],
                        data["humidity"]
                    )

    def show_data_on_table(self):
        """Hiển thị dữ liệu lên bảng sau khi kiểm tra tính hợp lệ."""
        city = self.inputThanhPho.text()
        temp = self.editNhietDo.text()
        wind_speed = self.editTocDoGio.text()
        humidity = self.editDoAm.text()

        # Kiểm tra dữ liệu trống
        if not all([city, temp, wind_speed, humidity]):
            QtWidgets.QMessageBox.warning(None, "Warning", "Dữ liệu không đầy đủ để thêm vào bảng!")
            return

        # Kiểm tra tính hợp lệ của dữ liệu
        is_valid, error_message = self.validate_data(temp, humidity)
        if not is_valid:
            QtWidgets.QMessageBox.warning(None, "Warning", error_message)
            return

        try:
            wind_speed_value = float(wind_speed.split()[0])
            if wind_speed_value < 0:
                QtWidgets.QMessageBox.warning(None, "Warning", "Tốc độ gió không thể âm!")
                return
        except (ValueError, IndexError):
            QtWidgets.QMessageBox.warning(None, "Warning", "Tốc độ gió không hợp lệ!")
            return

        # Nếu tất cả kiểm tra đều pass, thêm dữ liệu vào bảng
        self.add_row_to_table(city, temp, wind_speed, humidity)

    def add_row_to_table(self, city, temp, wind_speed, humidity):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(city))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(temp))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(wind_speed))
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(humidity))

    def visualization_sort_window(self):
        criteria = self.cbTieuChi.currentText()
        sort_method = self.cbLoaiSapXep.currentText()

        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])
            rows.append([city, temp, wind_speed, humidity])

        if criteria == "Nhiệt độ":
            key_index = 1
        elif criteria == "Tốc độ gió":
            key_index = 2
        elif criteria == "Độ ẩm":
            key_index = 3
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Tiêu chí không hợp lệ!")
            return

        try:
            if sort_method == "Selection Sort":
                values = [row[key_index] for row in rows]
                self.visualization_widget = SortVisualizationWidget(values, sort_type="select")
                self.visualization_widget.show()

            elif sort_method == "Quick Sort":
                values = [row[key_index] for row in rows]
                self.visualization_widget = SortVisualizationWidget(values, sort_type="quick")
                self.visualization_widget.show()

            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "Phương thức sắp xếp không hợp lệ!")
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return

    def sort_table_ascending(self):
        """Sắp xếp dữ liệu theo thứ tự tăng dần."""
        self.sort_table(order="ascending")

    def sort_table_descending(self):
        """Sắp xếp dữ liệu theo thứ tự giảm dần."""
        self.sort_table(order="descending")

    # Hiển thị dữ liệu được sắp xếp trong bảng
    def sort_table(self, order="ascending"):
        # Lấy tiêu chí và phương pháp sắp xếp đã chọn
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Selection Sort" or "Quick Sort"

        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  # Xóa đơn vị và chuyển về kiểu float
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])
            rows.append([city, temp, wind_speed, humidity])

        if criteria == "Nhiệt độ":
            key_index = 1
        elif criteria == "Tốc độ gió":
            key_index = 2
        elif criteria == "Độ ẩm":
            key_index = 3
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Tiêu chí không hợp lệ!")
            return

        # Chuyển đổi thứ tự sắp xếp
        ascending = order == "ascending"

        # Sử dụng time.perf_counter() cho việc tính toán thời gian thực thi của các thuật toán
        start_time = time.perf_counter()

        try:
            if sort_method == "Selection Sort":
                sorted_rows = selection_sort(rows, key_index, order)
                self.visualization_sort_window()

            elif sort_method == "Quick Sort":
                sorted_rows = quick_sort(rows, key_index, ascending)
                self.visualization_sort_window()

            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "Phương thức sắp xếp không hợp lệ!")
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return

        end_time = time.perf_counter()

        # Tính toán thời gian thực hiện
        elapsed_time = end_time - start_time

        # Hiển thị dữ liệu được sắp xếp trong bảng
        self.tableWidget.setRowCount(0)
        for row in sorted_rows:
            self.add_row_to_table(row[0], f"{row[1]:.2f} °C", f"{row[2]} m/s", f"{row[3]} %")

        QtWidgets.QMessageBox.information(None, "Sắp xếp hoàn tất", f"Thời gian sắp xếp: {elapsed_time:.6f} giây")

    def delete_selected_row(self):
        """Xóa hàng được chọn"""
        row = self.tableWidget.currentRow()
        if row >= 0:
            self.tableWidget.removeRow(row)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng chọn hàng để xóa!")

    def delete_all_rows(self):
        """Xóa tất cả các hàng trong bảng"""
        row_count = self.tableWidget.rowCount()
        if row_count > 0:
            self.tableWidget.setRowCount(0) 
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Bảng không có dữ liệu để xóa!")
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())