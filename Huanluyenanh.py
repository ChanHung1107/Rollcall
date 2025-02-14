import cv2
import numpy as np
import os

# Hàm để chuẩn bị dữ liệu huấn luyện (nếu cần)
def prepare_training_data(data_directory):
    faces = []
    labels = []

    if not os.path.exists(data_directory):
        print(f"Thư mục '{data_directory}' không tồn tại.")
        return faces, labels

    for label_dir in os.listdir(data_directory):
        label_dir_path = os.path.join(data_directory, label_dir)
        if os.path.isdir(label_dir_path):
            for image_file in os.listdir(label_dir_path):
                image_path = os.path.join(label_dir_path, image_file)
                if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"Không thể đọc ảnh: {image_path}")
                        continue

                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    faces.append(gray_image)
                    labels.append(int(label_dir.split('_')[1]))  # Lấy ID từ tên thư mục

    return faces, labels


# Đường dẫn đến file XML và thư mục chứa dữ liệu
model_file_path = 'face_recognition_model.xml'
data_directory = 'data'
print("Chuẩn bị dữ liệu huấn luyện...")
faces, labels = prepare_training_data(data_directory)

if len(faces) == 0 or len(labels) == 0:
    print("Không có dữ liệu để huấn luyện.")
else:
    print("Huấn luyện mô hình...")
    model = cv2.face.LBPHFaceRecognizer_create()

    # Huấn luyện mô hình
    model.train(faces, np.array(labels))

    # Lưu mô hình vào file
    model.save(model_file_path)

    print("Huấn luyện hoàn tất và mô hình đã được lưu.")

