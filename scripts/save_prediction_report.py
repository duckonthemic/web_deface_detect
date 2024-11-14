import os
import cv2
import numpy as np
import tensorflow as tf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Định nghĩa thư mục chứa các hình ảnh cần dự đoán
image_folder = 'test_images'
output_pdf = 'reports/prediction_report.pdf'

# Lấy danh sách các tệp hình ảnh trong thư mục
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model('models/web_defacement_model.h5')

# Định nghĩa các loại (class) của trang web
CATEGORIES = ['clean', 'defaced_type_1', 'defaced_type_2', 'defaced_type_3', 'defaced_type_4']

# Tạo canvas PDF
c = canvas.Canvas(output_pdf, pagesize=letter)

# Định dạng tiêu đề PDF
c.drawString(100, 750, "Prediction Report")
c.drawString(100, 730, "Predictions for images in 'test_images' folder:")

# Khởi tạo vị trí bắt đầu cho kết quả dự đoán
y_position = 710

# Dự đoán kết quả cho các hình ảnh
for image_name in image_files:
    image_path = os.path.join(image_folder, image_name)
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error: Unable to load image at {image_path}")
        continue

    img_resized = cv2.resize(img, (224, 224))  # Resize về kích thước phù hợp với mô hình
    img_resized = img_resized / 255.0  # Chuẩn hóa hình ảnh
    img_resized = np.expand_dims(img_resized, axis=0)  # Thêm chiều batch size

    # Dự đoán
    pred = model.predict(img_resized)
    predicted_class = np.argmax(pred, axis=1)  # Lấy class có xác suất cao nhất
    prediction_label = CATEGORIES[predicted_class[0]]

    # Ghi kết quả dự đoán vào PDF
    c.drawString(100, y_position, f"Image: {image_name} - Prediction: {prediction_label}")
    y_position -= 20  # Giảm vị trí y để hiển thị kết quả tiếp theo

    if y_position < 100:  # Kiểm tra nếu hết trang PDF
        c.showPage()
        y_position = 750  # Đặt lại vị trí y

# Lưu kết quả vào tệp PDF
c.save()

print(f"Prediction report saved to {output_pdf}")
