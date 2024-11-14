import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Đường dẫn đến các tệp đã được tiền xử lý
X_FILE = 'models/X.pickle'
Y_FILE = 'models/y.pickle'

# Đọc dữ liệu từ các tệp pickle
with open(X_FILE, 'rb') as f:
    X = pickle.load(f)
with open(Y_FILE, 'rb') as f:
    y = pickle.load(f)

# Chuyển đổi nhãn thành dạng one-hot encoding
y = to_categorical(y, num_classes=5)  # 5 classes: clean, defaced_type_1, defaced_type_2, defaced_type_3, defaced_type_4

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
model = Sequential()

# Thêm các lớp Convolutional và Pooling
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Thêm lớp Flatten và Dense cho mô hình
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(5, activation='softmax'))  # Sử dụng softmax cho đa lớp phân loại (clean + defaced)

# Biên dịch mô hình
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Lưu mô hình
model.save('models/web_defacement_model.h5')

# Vẽ biểu đồ độ chính xác và hàm mất mát
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

# Lưu và hiển thị các biểu đồ
plt.savefig('reports/training_performance.png')
plt.show()
