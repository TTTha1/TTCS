def selection_sort(data, key_index, order="ascending", start=0):
    n = len(data)
    if start >= n - 1:  # Điều kiện dừng của đệ quy
        return data

    # Tìm phần tử nhỏ nhất trong phần chưa sắp xếp bằng đệ quy
    def find_min_index(data, key_index, start, end, order):
        if start == end:
            return start
        min_index = find_min_index(data, key_index, start + 1, end, order)
        if (order == "ascending" and data[start][key_index] < data[min_index][key_index]) or \
           (order == "descending" and data[start][key_index] > data[min_index][key_index]):
            return start
        return min_index

    min_index = find_min_index(data, key_index, start, n - 1, order)

    # Hoán đổi phần tử nhỏ nhất với phần tử tại vị trí start
    data[start], data[min_index] = data[min_index], data[start]

    # Gọi đệ quy cho phần còn lại
    return selection_sort(data, key_index, order, start + 1)


def quick_sort(data, key_index, ascending=True):
    stack = [(0, len(data) - 1)]  # Sử dụng stack để thay thế đệ quy

    while stack:
        start, end = stack.pop()
        if start >= end:
            continue

        # Phân hoạch dữ liệu
        pivot = data[(start + end) // 2][key_index]
        left = start
        right = end

        while left <= right:
            while left <= right and ((ascending and data[left][key_index] < pivot) or (not ascending and data[left][key_index] > pivot)):
                left += 1
            while left <= right and ((ascending and data[right][key_index] > pivot) or (not ascending and data[right][key_index] < pivot)):
                right -= 1

            if left <= right:
                data[left], data[right] = data[right], data[left]
                left += 1
                right -= 1

        # Đưa các phần chưa được sắp xếp vào stack
        if start < right:
            stack.append((start, right))
        if left < end:
            stack.append((left, end))

    return data

