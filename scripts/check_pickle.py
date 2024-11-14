import pickle
import matplotlib.pyplot as plt

# Mở các tệp pickle để nạp dữ liệu
with open('models/X.pickle', 'rb') as f:
    X_loaded = pickle.load(f)  # Nạp dữ liệu hình ảnh

with open('models/y.pickle', 'rb') as f:
    y_loaded = pickle.load(f)  # Nạp nhãn

# Kiểm tra xem các tệp đã nạp có đúng không
print(f"Loaded X shape: {X_loaded.shape}")  # Kích thước của mảng X
print(f"Loaded y shape: {y_loaded.shape}")  # Kích thước của mảng y

# Hiển thị một số hình ảnh mẫu
for i in range(10):  # Hiển thị 10 hình ảnh mẫu
    plt.imshow(X_loaded[i])  # Hiển thị hình ảnh thứ i
    plt.title(f"Label: {y_loaded[i]}")  # Hiển thị nhãn
    plt.show()  # Hiển thị hình ảnh
