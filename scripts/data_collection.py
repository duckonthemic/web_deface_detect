import random
import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Đường dẫn thư mục lưu trữ ảnh
CLEAN_DIR = 'dataset/clean/'
DEFACED_DIR = 'dataset/defaced/'

# Danh sách các URL trang web mẫu
URLS = [
    'http://www.raci.it/component/user/reset.html',
    'http://www.vnic.co/',
    'http://www.rockabilly.it/'
]

# Định nghĩa các loại deface và script tương ứng
DEFACEMENT_SCRIPTS = {
    'defaced_type_1': "document.body.innerHTML = '<h1>Hacked by XYZ</h1><p>Your website has been defaced!</p>';",
    'defaced_type_2': """
        document.body.style.backgroundColor = 'black'; 
        document.body.style.color = 'yellow';
        document.body.style.filter = 'blur(5px)';
    """,
    'defaced_type_3': """
        var banner = document.createElement('div');
        banner.innerHTML = '<div style="background: red; color: white; text-align: center; padding: 10px;">Hacked by XYZ</div>';
        document.body.insertBefore(banner, document.body.firstChild);
    """,
    'defaced_type_4': """
        var mainContent = document.querySelector('main') || document.body;
        mainContent.innerHTML = '<h1 style="color: red; text-align: center;">Website compromised!</h1><p style="color: black;">This site has been taken over by malicious actors.</p>';
    """
}

# Tạo thư mục lưu ảnh nếu chưa tồn tại
if not os.path.exists(CLEAN_DIR):
    os.makedirs(CLEAN_DIR)

# Tạo các thư mục con cho từng loại deface
for deface_type in DEFACEMENT_SCRIPTS.keys():
    deface_path = os.path.join(DEFACED_DIR, deface_type)
    if not os.path.exists(deface_path):
        os.makedirs(deface_path)

# Khởi tạo WebDriver cho Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

# Hàm chụp ảnh màn hình trang web bình thường
def capture_clean_images(num_images=20):
    for i in range(num_images):
        url = random.choice(URLS)  # Lấy ngẫu nhiên một URL từ danh sách
        print(f"Capturing clean image {i} from {url}")  # In ra để kiểm tra
        driver.get(url)
        time.sleep(2)  # Chờ trang web tải xong
        screenshot_path = os.path.join(CLEAN_DIR, f'clean_{i}.png')
        driver.save_screenshot(screenshot_path)
        print(f'Saved clean image: {screenshot_path}')  # Thông báo ảnh clean đã lưu

# Hàm chụp ảnh màn hình trang web bị deface (nhiều kiểu defacement)
def capture_defaced_images(num_images=20):
    deface_types = list(DEFACEMENT_SCRIPTS.keys())
    for i in range(num_images):
        deface_type = random.choice(deface_types)  # Chọn ngẫu nhiên một loại deface
        script = DEFACEMENT_SCRIPTS[deface_type]
        url = random.choice(URLS)  # Lấy ngẫu nhiên một URL từ danh sách
        print(f"Executing deface script {i} ({deface_type}) on {url}")  # In ra để kiểm tra
        driver.get(url)
        time.sleep(2)  # Chờ trang web tải xong

        try:
            driver.execute_script(script)
        except Exception as e:
            print(f"Error executing script for {deface_type}: {e}")
            continue

        # Thêm thời gian chờ để chắc chắn rằng thay đổi đã được áp dụng
        time.sleep(3)

        # Lưu ảnh màn hình với tên khác nhau vào thư mục tương ứng
        screenshot_path = os.path.join(DEFACED_DIR, deface_type, f'defaced_{i}.png')
        driver.save_screenshot(screenshot_path)
        print(f'Saved defaced image: {screenshot_path}')  # Thông báo đã lưu ảnh defaced

# Chụp ảnh trang web bình thường và defaced với nhiều kiểu giả lập
capture_clean_images()
capture_defaced_images()

# Đóng trình duyệt
driver.quit()
