import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import img_to_array

# Nạp mô hình đã huấn luyện
model = load_model('models/web_defacement_model.h5')

# Đường dẫn đến thư mục chứa hình ảnh cần kiểm tra (test_images)
image_folder = 'test_images'

# Lấy danh sách các tệp hình ảnh trong thư mục test_images
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Định nghĩa các nhãn (label) cho các lớp
labels = ['clean', 'defaced_type_1', 'defaced_type_2', 'defaced_type_3', 'defaced_type_4']

# Dự đoán và hiển thị kết quả cho mỗi ảnh trong thư mục
for image_name in image_files:
    image_path = os.path.join(image_folder, image_name)
    
    # Đọc hình ảnh
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        continue  # Bỏ qua ảnh không đọc được
    
    # Chuyển đổi hình ảnh để mô hình có thể nhận diện
    img = cv2.resize(img, (224, 224))  # Đảm bảo kích thước ảnh giống như trong quá trình huấn luyện
    img = img / 255.0  # Chuẩn hóa ảnh
    img = np.expand_dims(img, axis=0)  # Thêm chiều batch size cho ảnh

    # Dự đoán
    prediction = model.predict(img)
    
    # Chọn nhãn có xác suất cao nhất
    predicted_class = np.argmax(prediction, axis=1)[0]
    predicted_label = labels[predicted_class]
    
    # In ra kết quả dự đoán
    print(f"Prediction for {image_name}: {predicted_label}")

    # Hiển thị ảnh và kết quả dự đoán
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    plt.title(f"Predicted: {predicted_label}")
    plt.show()
