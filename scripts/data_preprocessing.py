import os
import cv2
import numpy as np
import pickle
import random
import sys
from sklearn.model_selection import train_test_split

# Đảm bảo sys.stdout sử dụng mã hóa UTF-8
sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = 'dataset/'
CATEGORIES = ['clean', 'defaced/defaced_type_1', 'defaced/defaced_type_2', 'defaced/defaced_type_3', 'defaced/defaced_type_4']  # Các loại trang web
IMG_SIZE = 224

def create_dataset():
    data = []
    for category in CATEGORIES:
        path = os.path.join(DATA_DIR, category)
        if not os.path.exists(path):  # Kiểm tra thư mục có tồn tại hay không
            print(f"Thư mục {category} không tồn tại.")
            continue
        
        class_label = CATEGORIES.index(category)
        for img_name in os.listdir(path):
            try:
                img_path = os.path.join(path, img_name)
                img_array = cv2.imread(img_path)
                
                # Kiểm tra xem hình ảnh có được đọc thành công không
                if img_array is None:
                    print(f"Lỗi khi đọc ảnh {img_path}")
                    continue
                
                resized_img = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                data.append([resized_img, class_label])
            except Exception as e:
                print(f"Lỗi khi xử lý ảnh {img_name}: {e}")
    return data

# Tạo dataset và lưu trữ
dataset = create_dataset()
print(f"Tổng số mẫu: {len(dataset)}")

# Nếu không có dữ liệu, thông báo lỗi
if len(dataset) == 0:
    print("Không có dữ liệu để huấn luyện.")
    sys.exit(1)

# Shuffle dữ liệu
random.shuffle(dataset)

# Tách features và labels
X = []
y = []

for features, label in dataset:
    X.append(features)
    y.append(label)

# Chuyển sang numpy array và chuẩn hóa
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3) / 255.0
y = np.array(y)

# Tách dữ liệu thành train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Lưu dữ liệu đã tiền xử lý
try:
    os.makedirs('models', exist_ok=True)
    with open('models/X.pickle', 'wb') as f:
        pickle.dump(X, f)
    with open('models/y.pickle', 'wb') as f:
        pickle.dump(y, f)
    print("Dữ liệu đã được lưu vào tệp 'models/X.pickle' và 'models/y.pickle'.")
except Exception as e:
    print(f"Lỗi khi lưu tệp: {e}")
