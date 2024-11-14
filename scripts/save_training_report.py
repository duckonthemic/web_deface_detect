from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np
import pickle
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Đọc dữ liệu từ các tệp pickle
X_FILE = 'models/X.pickle'
Y_FILE = 'models/y.pickle'

# Đọc dữ liệu
with open(X_FILE, 'rb') as f:
    X = pickle.load(f)
with open(Y_FILE, 'rb') as f:
    y = pickle.load(f)

# Chuyển đổi nhãn thành dạng one-hot encoding
y = to_categorical(y, num_classes=5)

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
model = tf.keras.Sequential()

# Thêm các lớp Convolutional và Pooling
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Conv2D(128, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))

# Thêm lớp Flatten và Dense cho mô hình
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(5, activation='softmax'))  # Phân loại 5 lớp

# Biên dịch mô hình
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Lưu mô hình
model.save('models/web_defacement_model.h5')

# Lưu kết quả huấn luyện vào PDF
pdf_filename = 'reports/training_report.pdf'
c = canvas.Canvas(pdf_filename, pagesize=letter)

# Lưu kết quả huấn luyện vào PDF
c.drawString(100, 750, "Training Report")
c.drawString(100, 730, f"Epochs: {10}")
c.drawString(100, 710, f"Train Accuracy: {history.history['accuracy'][-1]:.4f}")
c.drawString(100, 690, f"Test Accuracy: {history.history['val_accuracy'][-1]:.4f}")

# Dự đoán kết quả cho các hình ảnh
c.drawString(100, 670, "Prediction Results:")

# Lưu biểu đồ độ chính xác và hàm mất mát vào PDF
plt.figure(figsize=(12, 6))

# Biểu đồ độ chính xác
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Huấn luyện')
plt.plot(history.history['val_accuracy'], label='Kiểm tra')
plt.legend()
plt.title('Độ chính xác')

# Biểu đồ hàm mất mát
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Huấn luyện')
plt.plot(history.history['val_loss'], label='Kiểm tra')
plt.legend()
plt.title('Hàm mất mát')

# Lưu biểu đồ vào file PNG
plot_filename = 'reports/training_performance.png'
plt.savefig(plot_filename)

# Thêm ảnh biểu đồ vào PDF
c.drawImage(plot_filename, 100, 400, width=400, height=200)

# Lưu PDF
c.save()

# Hiển thị biểu đồ
plt.show()
