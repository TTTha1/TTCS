from PyQt6 import QtCore, QtGui, QtWidgets
import time

class SortVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, data, sort_type="select", parent=None):
        super().__init__(parent)
        self.data = data
        self.sort_type = sort_type
        self.ascending = True  # Mặc định là sắp xếp tăng dần
        self.animation_speed = 0.5  # Tốc độ di chuyển
        self.setWindowTitle("Sắp Xếp Trực Quan")
        self.resize(700, 500)

        # Scene và View để vẽ biểu đồ
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 680, 380)

        # Các nút để chọn thuật toán và bắt đầu
        self.start_button = QtWidgets.QPushButton("Bắt đầu Sắp Xếp", self)
        self.start_button.setGeometry(10, 360, 200, 30)
        self.start_button.clicked.connect(self.start_sorting)

        # Nút radio để chọn sắp xếp tăng dần/giảm dần
        self.ascending_radio = QtWidgets.QRadioButton("Tăng dần", self)
        self.ascending_radio.setGeometry(220, 450, 100, 30)
        self.ascending_radio.setChecked(True)
        self.ascending_radio.toggled.connect(self.update_sort_order)
        self.descending_radio = QtWidgets.QRadioButton("Giảm dần", self)
        self.descending_radio.setGeometry(320, 450, 100, 30)

        self.draw_data(self.data, ['blue' for _ in range(len(self.data))])

    def update_sort_order(self):
        """Cập nhật chế độ sắp xếp"""
        self.ascending = self.ascending_radio.isChecked()

    def draw_data(self, data, color_array):
        """Vẽ biểu đồ cột từ dữ liệu và tô màu cột (hỗ trợ giá trị âm)"""
        self.scene.clear()
        c_height = 360
        c_width = 680
        x_width = c_width / (len(data) + 1)
        offset = 20
        spacing = 5

        max_value = max(map(abs, data))  # Lấy giá trị tuyệt đối lớn nhất
        zero_line = c_height / 2  # Đường trung tâm cho giá trị 0

        for i, value in enumerate(data):
            normalized_height = abs(value) / max_value  # Chiều cao chuẩn hóa
            height = normalized_height * (c_height / 2 - 10)  # Chiều cao cột

            # Tính tọa độ Y cho cột
            if value >= 0:
                y0 = zero_line - height
            else:
                y0 = zero_line

            # Vị trí X và kích thước cột
            x0 = i * x_width + offset + spacing
            x1 = x_width - spacing
            y1 = height

            # Vẽ cột và tô màu
            rect = QtWidgets.QGraphicsRectItem(x0, y0, x1, y1)
            rect.setBrush(QtGui.QColor(color_array[i]))
            self.scene.addItem(rect)

            # Hiển thị giá trị lên cột (canh chỉnh đúng vị trí)
            text = QtWidgets.QGraphicsTextItem(str(value))
            if value >= 0:
                text.setPos(x0 + spacing, y0 - 20)
            else:
                text.setPos(x0 + spacing, y0 + height + 5)
            self.scene.addItem(text)

        # Vẽ đường trung tâm (giá trị 0)
        zero_line_pen = QtGui.QPen(QtGui.QColor("black"), 2)
        self.scene.addLine(offset, zero_line, c_width, zero_line, zero_line_pen)

    def selection_sort_recursive(self, data, start=0):
        """Sắp xếp chọn đệ quy với trực quan hóa"""
        n = len(data)

        # Trường hợp cơ sở: Nếu đã đến cuối danh sách, kết thúc
        if start >= n - 1:
            # Vẽ mảng đã sắp xếp cuối cùng
            self.draw_data(data, ['green' for _ in range(len(data))])
            return

        # Tìm chỉ số của phần tử nhỏ nhất trong mảng con bằng cách sử dụng đệ quy
        min_index = self.find_min_index(data, start, start + 1)

        # Trực quan hóa so sánh và lựa chọn
        color_array = ['orange' if k == start or k == min_index else 'blue' for k in range(n)]
        self.draw_data(data, color_array)
        QtCore.QCoreApplication.processEvents()
        time.sleep(self.animation_speed)

        # Hoán đổi phần tử hiện tại với phần tử nhỏ nhất nếu cần
        if min_index != start:
            data[start], data[min_index] = data[min_index], data[start]

        # Trực quan hóa mảng sau khi cập nhật
        color_array = ['green' if k <= start else 'blue' for k in range(n)]
        self.draw_data(data, color_array)
        QtCore.QCoreApplication.processEvents()
        time.sleep(self.animation_speed)

        # Gọi đệ quy cho phần mảng còn lại
        self.selection_sort_recursive(data, start + 1)

    def find_min_index(self, data, current_min, index):
        """Tìm chỉ số của phần tử nhỏ/lớn nhất trong mảng bằng cách sử dụng đệ quy"""
        # Trường hợp cơ sở: Nếu index đạt đến cuối danh sách, trả về chỉ số phần tử nhỏ/lớn nhất hiện tại
        if index >= len(data):
            return current_min

        # Cập nhật chỉ số phần tử nhỏ/lớn nhất hiện tại tùy theo chế độ
        if (self.ascending and data[index] < data[current_min]) or (not self.ascending and data[index] > data[current_min]):
            current_min = index

        # Tiếp tục đệ quy
        return self.find_min_index(data, current_min, index + 1)

    def quick_sort_visualization(self, data):
        """Quick Sort không đệ quy với cập nhật biểu đồ"""
        stack = [(0, len(data) - 1)]  # Khởi tạo ngăn xếp với phạm vi ban đầu
        color_array = ['blue' for _ in range(len(data))]  # Màu sắc ban đầu

        while stack:
            left, right = stack.pop()

            if left < right:
                # Phân hoạch mảng và lấy chỉ số phân chia
                pivot_index = self.partition(data, left, right, color_array)

                # Đẩy các đoạn mảng chưa sắp xếp vào stack
                stack.append((left, pivot_index - 1))  # Nửa bên trái
                stack.append((pivot_index, right))    # Nửa bên phải

        # Vẽ biểu đồ hoàn thành sau khi sắp xếp
        self.draw_data(data, ['green' for _ in range(len(data))])

    def partition(self, data, left, right, color_array):
        """Hàm phân hoạch mảng với pivot là phần tử giữa"""
        pivot_index = (left + right) // 2  # Pivot là phần tử giữa
        pivot_value = data[pivot_index]
        l, r = left, right

        while l <= r:
            # Đánh dấu các phần tử đang so sánh và pivot
            color_array_copy = color_array[:]
            color_array_copy[pivot_index] = 'purple'  # Pivot
            color_array_copy[l] = 'orange'         # Đang so sánh từ bên trái
            color_array_copy[r] = 'orange'         # Đang so sánh từ bên phải

            self.draw_data(data, color_array_copy)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed)

            # Di chuyển con trỏ l hoặc r dựa trên thứ tự sắp xếp
            if self.ascending:
                while data[l] < pivot_value:
                    l += 1
                while data[r] > pivot_value:
                    r -= 1
            else:
                while data[l] > pivot_value:
                    l += 1
                while data[r] < pivot_value:
                    r -= 1

            # Hoán đổi các phần tử nếu cần thiết
            if l <= r:
                data[l], data[r] = data[r], data[l]
                l += 1
                r -= 1

                # Vẽ lại khi có sự hoán đổi
                color_array_copy = ['blue' for _ in range(len(data))]
                color_array_copy[l - 1] = 'green'  # Đánh dấu phần tử đã hoán đổi bên trái
                color_array_copy[r + 1] = 'green'  # Đánh dấu phần tử đã hoán đổi bên phải
                self.draw_data(data, color_array_copy)
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed)

        # Vẽ lại mảng sau khi hoàn tất phân hoạch
        color_array_copy = ['blue' for _ in range(len(data))]
        color_array_copy[pivot_index] = 'purple'  # Pivot giữ nguyên màu
        self.draw_data(data, color_array_copy)
        QtCore.QCoreApplication.processEvents()
        time.sleep(self.animation_speed)

        return l  # Trả về chỉ số bắt đầu phân hoạch tiếp theo


    def start_sorting(self):
        """Khởi chạy thuật toán sắp xếp theo loại"""
        if self.sort_type == "select":
            self.selection_sort_recursive(self.data)
        elif self.sort_type == "quick":
            self.quick_sort_visualization(self.data)

