from PyQt6 import QtCore, QtGui, QtWidgets
import time

class SortVisualizationWidget(QtWidgets.QWidget):
    def __init__(self, data, sort_type="bubble", parent=None):
        super().__init__(parent)
        self.data = data
        self.sort_type = sort_type
        self.animation_speed = 0.2  # Tốc độ hoạt hình
        self.setWindowTitle("Sắp Xếp Trực Quan")
        self.resize(700, 400)

        # Scene và View để vẽ biểu đồ
        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.setGeometry(10, 10, 680, 380)

        # Các nút để chọn thuật toán và bắt đầu
        self.start_button = QtWidgets.QPushButton("Bắt đầu Sắp Xếp", self)
        self.start_button.setGeometry(10, 360, 200, 30)
        self.start_button.clicked.connect(self.start_sorting)

        self.draw_data(self.data, ['red' for _ in range(len(self.data))])

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

    def selection_sort_visualization(self, data):
        """Selection Sort với cập nhật biểu đồ"""
        n = len(data)
        for i in range(n - 1):
            min_index = i  # Giả sử phần tử nhỏ nhất là i
            for j in range(i + 1, n):
                # So sánh và tìm phần tử nhỏ hơn
                color_array = ['yellow' if k == i or k == j else 'red' for k in range(n)]  # Đánh dấu các phần tử đang so sánh
                self.draw_data(data, color_array)
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed)

                if data[j] < data[min_index]:
                    min_index = j
            
            # Hoán đổi nếu cần thiết
            if min_index != i:
                data[i], data[min_index] = data[min_index], data[i]

            # Cập nhật màu sắc sau khi hoán đổi
            color_array = ['green' if k <= i else 'red' for k in range(n)]  # Đánh dấu các phần tử đã được sắp xếp
            self.draw_data(data, color_array)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed)
        
        # Vẽ biểu đồ hoàn thành sau khi sắp xếp
        self.draw_data(data, ['green' for _ in range(len(data))])

    def quick_sort_visualization(self, data):
        """Quick Sort với cập nhật biểu đồ"""
        color_array = ['red' for _ in range(len(data))]  # Màu ban đầu của mảng
        self.quick_sort_step(data, 0, len(data) - 1, color_array)
        # Vẽ biểu đồ hoàn thành sau khi sắp xếp
        self.draw_data(data, ['green' for _ in range(len(data))])

    def quick_sort_step(self, data, left, right, color_array):
        """Phân chia và gọi đệ quy Quick Sort"""
        if left < right:
            # Phân hoạch mảng và lấy chỉ số phân chia
            pivot_index = self.partition(data, left, right, color_array)

            # Đệ quy sắp xếp hai nửa (trừ pivot)
            self.quick_sort_step(data, left, pivot_index - 1, color_array)  # Nửa bên trái
            self.quick_sort_step(data, pivot_index, right, color_array)  # Nửa bên phải

    def partition(self, data, left, right, color_array):
        """Hàm phân hoạch mảng với pivot là phần tử giữa và giữ nguyên vị trí"""
        pivot_index = (left + right) // 2  # Chọn pivot là phần tử giữa
        pivot_value = data[pivot_index]
        l, r = left, right

        while l <= r:
            # Đánh dấu các phần tử đang so sánh và pivot
            color_array_copy = color_array[:]
            color_array_copy[pivot_index] = 'blue'  # Pivot
            color_array_copy[l] = 'yellow'  # Đang so sánh từ bên trái
            color_array_copy[r] = 'yellow'  # Đang so sánh từ bên phải

            self.draw_data(data, color_array_copy)
            QtCore.QCoreApplication.processEvents()
            time.sleep(self.animation_speed)

            # Di chuyển con trỏ l sang phải nếu nhỏ hơn pivot
            while data[l] < pivot_value:
                l += 1
            # Di chuyển con trỏ r sang trái nếu lớn hơn pivot
            while data[r] > pivot_value:
                r -= 1

            # Hoán đổi các phần tử nếu cần thiết
            if l <= r:
                data[l], data[r] = data[r], data[l]
                l += 1
                r -= 1

                # Vẽ lại khi có sự hoán đổi
                color_array_copy = ['red' for _ in range(len(data))]
                color_array_copy[l - 1] = 'green'  # Đánh dấu phần tử đã hoán đổi bên trái
                color_array_copy[r + 1] = 'green'  # Đánh dấu phần tử đã hoán đổi bên phải
                self.draw_data(data, color_array_copy)
                QtCore.QCoreApplication.processEvents()
                time.sleep(self.animation_speed)

        # Vẽ lại mảng sau khi hoàn tất phân hoạch
        color_array_copy = ['red' for _ in range(len(data))]
        color_array_copy[pivot_index] = 'blue'  # Pivot giữ nguyên màu
        self.draw_data(data, color_array_copy)
        QtCore.QCoreApplication.processEvents()
        time.sleep(self.animation_speed)

        return l  # Trả về chỉ số bắt đầu phân hoạch tiếp theo

    def start_sorting(self):
        """Khởi chạy thuật toán sắp xếp theo loại"""
        if self.sort_type == "select":
            self.selection_sort_visualization(self.data)
        elif self.sort_type == "quick":
            self.quick_sort_visualization(self.data)

