from PyQt6 import QtCore, QtGui, QtWidgets
from VisualizationSort import *
import requests, json, timeit
from SortingAlgorithm import selection_sort, quick_sort

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.buttonDeleteRow = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteRow.setGeometry(QtCore.QRect(10, 550, 131, 28))
        self.buttonDeleteRow.setObjectName("buttonDeleteRow")
        self.buttonDeleteAll = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonDeleteAll.setGeometry(QtCore.QRect(170, 550, 111, 28))
        self.buttonDeleteAll.setObjectName("buttonDeleteAll")
        #
        self.buttonVisualizationSort = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonVisualizationSort.setGeometry(QtCore.QRect(330, 550, 93, 28))
        self.buttonVisualizationSort.setObjectName("buttonVisualizationSort")
        self.buttonSort = QtWidgets.QPushButton(parent=self.centralwidget)
        self.buttonSort.setGeometry(QtCore.QRect(480, 550, 93, 28))
        self.buttonSort.setObjectName("buttonSort")
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
        self.rbTrucTiep = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbTrucTiep.setGeometry(QtCore.QRect(60, 50, 151, 20))
        self.rbTrucTiep.setObjectName("rbTrucTiep")
        self.rbFile = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbFile.setGeometry(QtCore.QRect(220, 50, 171, 20))
        self.rbFile.setObjectName("rbFile")
        self.rbNhapTay = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.rbNhapTay.setGeometry(QtCore.QRect(410, 50, 95, 20))
        self.rbNhapTay.setObjectName("rbNhapTay")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(330, 100, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(330, 140, 71, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(340, 180, 55, 16))
        self.label_3.setObjectName("label_3")
        self.editNhietDo = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editNhietDo.setGeometry(QtCore.QRect(420, 100, 113, 22))
        self.editNhietDo.setReadOnly(True)
        self.editNhietDo.setObjectName("editNhietDo")
        self.editTocDoGio = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editTocDoGio.setGeometry(QtCore.QRect(420, 140, 113, 22))
        self.editTocDoGio.setReadOnly(True)
        self.editTocDoGio.setObjectName("editTocDoGio")
        self.editDoAm = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.editDoAm.setGeometry(QtCore.QRect(420, 180, 113, 22))
        self.editDoAm.setReadOnly(True)
        self.editDoAm.setObjectName("editDoAm")
        self.inputThanhPho = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.inputThanhPho.setGeometry(QtCore.QRect(20, 90, 113, 22))
        self.inputThanhPho.setObjectName("inputThanhPho")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 90, 111, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(270, 230, 141, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(180, 300, 440, 201))
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
        # Connect rbNhapTay toggle signal to a method
        self.rbNhapTay.toggled.connect(self.enable_manual_input)
        # Connect pushButton click to fetch weather data
        self.pushButton.clicked.connect(self.fetch_weather_data)
        # Connect pushButton_2 click to show data on table
        self.pushButton_2.clicked.connect(self.show_data_on_table)
        #
        self.buttonDeleteRow.clicked.connect(self.delete_selected_row)
        self.buttonDeleteAll.clicked.connect(self.delete_all_rows)
        self.buttonSort.clicked.connect(self.sort_table)
        self.buttonVisualizationSort.clicked.connect(self.visualization_sort_window)
        #
        self.sortVisualizationWindow = None  # Reference for sorting visualization window
      
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.buttonDeleteRow.setText(_translate("MainWindow", "Xóa hàng đang chọn"))
        self.buttonDeleteAll.setText(_translate("MainWindow", "Xóa tất cả hàng"))
        self.buttonVisualizationSort.setText(_translate("MainWindow", "Trực quan"))
        self.buttonSort.setText(_translate("MainWindow", "Sắp xếp"))
        self.cbTieuChi.setItemText(0, _translate("MainWindow", "Nhiệt độ"))
        self.cbTieuChi.setItemText(1, _translate("MainWindow", "Tốc độ gió"))
        self.cbTieuChi.setItemText(2, _translate("MainWindow", "Độ ẩm"))
        self.cbLoaiSapXep.setItemText(0, _translate("MainWindow", "Selection Sort"))
        self.cbLoaiSapXep.setItemText(1, _translate("MainWindow", "Quick Sort"))
        self.rbTrucTiep.setText(_translate("MainWindow", "Lấy dữ liệu trực tiếp"))
        self.rbFile.setText(_translate("MainWindow", "Lấy dữ liệu từ file có sẵn"))
        self.rbNhapTay.setText(_translate("MainWindow", "Nhập tay"))
        self.label.setText(_translate("MainWindow", "Nhiệt độ"))
        self.label_2.setText(_translate("MainWindow", "Tốc độ gió"))
        self.label_3.setText(_translate("MainWindow", "Độ ẩm"))
        self.pushButton.setText(_translate("MainWindow", "Nhập Thành Phố"))
        self.pushButton_2.setText(_translate("MainWindow", "Hiện Kết Quả Lên Bảng"))
    def enable_manual_input(self, checked):
        """Enable or disable manual input based on rbNhapTay state."""
        if checked:  # If rbNhapTay is selected
            self.editNhietDo.setReadOnly(False)
            self.editTocDoGio.setReadOnly(False)
            self.editDoAm.setReadOnly(False)
        else:  # Reset to read-only if rbNhapTay is deselected
            self.editNhietDo.setReadOnly(True)
            self.editTocDoGio.setReadOnly(True)
            self.editDoAm.setReadOnly(True)

    def fetch_weather_data(self):
        """Fetch weather data from API and display in the fields."""
        if self.rbTrucTiep.isChecked():
            city = self.inputThanhPho.text()
            if not city:
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập tên thành phố!")
                return
            API_KEY = "bd64ba52f144248132813357b07e5338"
            BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
            try:
                url = BASE_URL + f"appid={API_KEY}&q={city}"
                response = requests.get(url).json()

                if response.get("cod") != 200:
                    QtWidgets.QMessageBox.critical(None, "Error", f"Không tìm thấy thành phố: {city}")
                    return
                # Extract weather data
                temp_kelvin = response["main"]["temp"]
                humidity = response["main"]["humidity"]
                wind_speed = response["wind"]["speed"]
                # Convert temperature to Celsius
                temp_celsius = temp_kelvin - 273.15
                # Display data in the fields
                self.editNhietDo.setText(f"{temp_celsius:.2f} °C")
                self.editTocDoGio.setText(f"{wind_speed} m/s")
                self.editDoAm.setText(f"{humidity} %")
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Đã xảy ra lỗi: {e}")
    def show_data_on_table(self):
        """Display the data on the table widget."""
        city = self.inputThanhPho.text()

        # Get the values based on selected radio button
        if self.rbTrucTiep.isChecked():
            temp = self.editNhietDo.text()
            wind_speed = self.editTocDoGio.text()
            humidity = self.editDoAm.text()

            # Check if the data is available
            if not temp or not wind_speed or not humidity:
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng lấy dữ liệu trước khi hiển thị lên bảng!")
                return
            self.add_row_to_table(city, temp, wind_speed, humidity)

        elif self.rbFile.isChecked():
            # Code for reading data from a JSON file
            try:
                # Open and read the JSON file
                with open("weather_data10.json", "r", encoding="utf-8") as file:
                    data = json.load(file)

                    # Loop through the data and add it to the table
                    for item in data:
                        # Extract data for each city
                        city = item.get("name")
                        temp_kelvin = item.get("main", {}).get("temp")
                        wind_speed = item.get("wind", {}).get("speed")
                        humidity = item.get("main", {}).get("humidity")

                        # Check if all necessary data is available
                        if city and temp_kelvin is not None and wind_speed is not None and humidity is not None:
                            # Convert temperature from Kelvin to Celsius
                            temp_celsius = temp_kelvin - 273.15

                            # Add to table
                            self.add_row_to_table(city, f"{temp_celsius:.2f} °C", f"{wind_speed} m/s", f"{humidity} %")
                        else:
                            QtWidgets.QMessageBox.warning(None, "Warning", "Dữ liệu không đầy đủ trong file JSON!")
                            return

            except FileNotFoundError:
                QtWidgets.QMessageBox.warning(None, "Error", "Không tìm thấy file dữ liệu!")
                return
            except json.JSONDecodeError:
                QtWidgets.QMessageBox.warning(None, "Error", "Lỗi định dạng file JSON!")
                return
            except Exception as e:
                QtWidgets.QMessageBox.warning(None, "Error", f"Đã xảy ra lỗi khi đọc file: {e}")
                return

        elif self.rbNhapTay.isChecked():
            # Get manually entered data
            temp = self.editNhietDo.text()
            wind_speed = self.editTocDoGio.text()
            humidity = self.editDoAm.text()

            # Check if the user entered all the required data
            if not temp or not wind_speed or not humidity:
                QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng nhập đầy đủ dữ liệu!")
                return
            self.add_row_to_table(city, temp, wind_speed, humidity)

    def add_row_to_table(self, city, temp, wind_speed, humidity):
        """Add a new row to the table."""
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)

        # Add data to the row
        self.tableWidget.setItem(row_position, 0, QtWidgets.QTableWidgetItem(city))
        self.tableWidget.setItem(row_position, 1, QtWidgets.QTableWidgetItem(temp))
        self.tableWidget.setItem(row_position, 2, QtWidgets.QTableWidgetItem(wind_speed))
        self.tableWidget.setItem(row_position, 3, QtWidgets.QTableWidgetItem(humidity))
    def visualization_sort_window(self):
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Selection Sort" or "Quick Sort"

        # Convert table data to a list of tuples for sorting
        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  # Remove the unit and convert to float
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])  # Remove unit and convert to float
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])  # Remove unit and convert to float
            rows.append([city, temp, wind_speed, humidity])

        # Choose the sorting key based on the selected criteria
        if criteria == "Nhiệt độ":
            key_index = 1  # Sort by temperature
        elif criteria == "Tốc độ gió":
            key_index = 2  # Sort by wind speed
        elif criteria == "Độ ẩm":
            key_index = 3  # Sort by humidity
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Tiêu chí không hợp lệ!")
            return

        # Sort the data based on the chosen method
        try:
            if sort_method == "Selection Sort":
                # Visualize sorting if Selection Sort is selected
                values = [row[key_index] for row in rows]  # Extract column values to sort
                self.visualization_widget = SortVisualizationWidget(values, sort_type="select")
                self.visualization_widget.show()

            elif sort_method == "Quick Sort":
                # Visualize sorting if Merge Sort is selected
                values = [row[key_index] for row in rows]  # Extract column values to sort
                self.visualization_widget = SortVisualizationWidget(values, sort_type="quick")
                self.visualization_widget.show()

            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "Phương thức sắp xếp không hợp lệ!")
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return


        # Display the sorted data in the table
        
    def sort_table(self):
        """Sort the data in the table according to the selected criteria."""
        # Get the selected sorting criterion and method
        criteria = self.cbTieuChi.currentText()  # "Nhiệt độ", "Tốc độ gió", "Độ ẩm"
        sort_method = self.cbLoaiSapXep.currentText()  # "Selection Sort" or "Quick Sort"

        # Convert table data to a list of tuples for sorting
        rows = []
        for row in range(self.tableWidget.rowCount()):
            city = self.tableWidget.item(row, 0).text()
            temp = float(self.tableWidget.item(row, 1).text().split()[0])  # Remove the unit and convert to float
            wind_speed = float(self.tableWidget.item(row, 2).text().split()[0])  # Remove unit and convert to float
            humidity = float(self.tableWidget.item(row, 3).text().split()[0])  # Remove unit and convert to float
            rows.append([city, temp, wind_speed, humidity])

        # Choose the sorting key based on the selected criteria
        if criteria == "Nhiệt độ":
            key_index = 1  # Sort by temperature
        elif criteria == "Tốc độ gió":
            key_index = 2  # Sort by wind speed
        elif criteria == "Độ ẩm":
            key_index = 3  # Sort by humidity
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Tiêu chí không hợp lệ!")
            return

        # Start the timer using time.perf_counter() for high precision
        start_time = timeit.default_timer()

        # Sort the data based on the chosen method
        try:
            if sort_method == "Selection Sort":
                sorted_rows = selection_sort(rows, key_index)
            elif sort_method == "Quick Sort":
                sorted_rows = quick_sort(rows, key_index)
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", "Phương thức sắp xếp không hợp lệ!")
                return
        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "Error", f"Đã có lỗi xảy ra: {str(e)}")
            return

        # End the timer
        end_time = timeit.default_timer()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Display the sorted data in the table
        self.tableWidget.setRowCount(0)
        for row in sorted_rows:
            self.add_row_to_table(row[0], f"{row[1]:.2f} °C", f"{row[2]} m/s", f"{row[3]} %")

        # Show a message box with the sorting time
        QtWidgets.QMessageBox.information(None, "Sắp xếp hoàn tất", f"Thời gian sắp xếp: {elapsed_time:.6f} giây") 
                

    def delete_selected_row(self):
        """Delete the selected row in the table."""
        row = self.tableWidget.currentRow()
        if row >= 0:  # Ensure a row is selected
            self.tableWidget.removeRow(row)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", "Vui lòng chọn hàng để xóa!")

    def delete_all_rows(self):
        """Delete all rows in the table."""
        row_count = self.tableWidget.rowCount()
        if row_count > 0:
            self.tableWidget.setRowCount(0)  # Set row count to 0, which removes all rows
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