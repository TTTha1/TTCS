# sort.py

def selection_sort(data, key_index):
    n = len(data)
    # Duyệt qua từng phần tử trong mảng
    for i in range(n):
        # Tìm phần tử nhỏ nhất trong phần chưa sắp xếp
        min_index = i
        for j in range(i + 1, n):
            # So sánh dữ liệu ở cột key_index
            if data[j][key_index] < data[min_index][key_index]:
                min_index = j
        
        # Hoán đổi phần tử nhỏ nhất với phần tử tại vị trí i
        data[i], data[min_index] = data[min_index], data[i]
    
    return data




def merge(left, right, key_index):
    result = []
    i = j = 0

    # Gộp hai danh sách left và right theo key_index
    while i < len(left) and j < len(right):
        if left[i][key_index] < right[j][key_index]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Nếu còn phần tử trong left
    while i < len(left):
        result.append(left[i])
        i += 1

    # Nếu còn phần tử trong right
    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort(data, key_index):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left_half = data[:mid]
    right_half = data[mid:]

    # Đệ quy sắp xếp hai nửa
    left_sorted = merge_sort(left_half, key_index)
    right_sorted = merge_sort(right_half, key_index)

    # Gộp hai nửa đã sắp xếp
    return merge(left_sorted, right_sorted, key_index)

def partition(data, key_index):
    pivot = data[len(data) // 2]  # Chọn pivot là phần tử ở giữa
    left = []
    right = []
    equal = []

    # Phân chia dữ liệu thành 3 phần: nhỏ hơn, lớn hơn và bằng pivot
    for item in data:
        if item[key_index] < pivot[key_index]:
            left.append(item)
        elif item[key_index] > pivot[key_index]:
            right.append(item)
        else:
            equal.append(item)

    return left, equal, right


def quick_sort(data, key_index):
    # Trường hợp cơ bản: nếu dữ liệu có 1 phần tử hoặc rỗng thì trả về ngay
    if len(data) <= 1:
        return data

    # Phân chia dữ liệu
    left, equal, right = partition(data, key_index)

    # Đệ quy sắp xếp phần nhỏ hơn và lớn hơn
    sorted_left = quick_sort(left, key_index)
    sorted_right = quick_sort(right, key_index)

    # Gộp lại kết quả
    return sorted_left + equal + sorted_right