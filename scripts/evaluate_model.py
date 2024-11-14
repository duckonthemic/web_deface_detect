import tensorflow as tf
import numpy as np
import pickle
import os
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Tải dữ liệu huấn luyện và kiểm tra từ các tệp pickle
with open('models/X.pickle', 'rb') as f:
    X_train = pickle.load(f)
with open('models/y.pickle', 'rb') as f:
    y_train = pickle.load(f)

# Tạo dữ liệu kiểm tra (có thể chia từ X_train và y_train hoặc dữ liệu riêng biệt)
X_test = X_train[-20:]  # Giả sử lấy 20% cuối làm dữ liệu kiểm tra
y_test = y_train[-20:]

# Tải mô hình đã huấn luyện
model = tf.keras.models.load_model('models/web_defacement_model.h5')

# Dự đoán kết quả trên tập kiểm tra
y_pred = model.predict(X_test)

# Chuyển kết quả dự đoán thành nhãn (bảng phân loại)
y_pred_class = np.argmax(y_pred, axis=1)  # Chọn lớp có xác suất cao nhất

# Tạo báo cáo phân loại
target_names = ['clean', 'defaced_type_1', 'defaced_type_2', 'defaced_type_3', 'defaced_type_4']
report = classification_report(y_test, y_pred_class, target_names=target_names)

# In ra báo cáo phân loại
print("\nClassification Report:")
print(report)

# Tạo ma trận nhầm lẫn (Confusion Matrix)
cm = confusion_matrix(y_test, y_pred_class)

# Vẽ ma trận nhầm lẫn
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=target_names, yticklabels=target_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.show()

# Lưu báo cáo phân loại vào một tệp
with open('reports/classification_report.txt', 'w') as f:
    f.write("Classification Report:\n")
    f.write(report)
    f.write("\nConfusion Matrix:\n")
    f.write(str(cm))

print("Classification report and confusion matrix have been saved to 'reports/classification_report.txt'")
