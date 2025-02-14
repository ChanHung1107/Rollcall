import cv2
import csv
import os  # Import os for file operations

# Đọc mô hình đã huấn luyện
model = cv2.face.LBPHFaceRecognizer_create()
model.read('face_recognition_model.xml')

# Đọc ánh xạ ID, tên và MSSV từ tệp
id_to_name_mssv = {}
with open('id_name_mssv.txt', 'r', encoding='utf-8') as file:
    for line in file:
        id, name, mssv = line.strip().split(',')
        id_to_name_mssv[int(id)] = (name, mssv)

# Khởi tạo webcam và cascade classifier
camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Thiết lập ngưỡng độ tin cậy
confidence_threshold = 55

# Xóa file CSV cũ nếu tồn tại và tạo mới
csv_file_path = 'diemdanh.csv'
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)  # Xóa file cũ

# Tạo file CSV và tiêu đề
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["MSSV", "Tensv", "DiemDanh"])

# Hàm kiểm tra xem MSSV đã điểm danh chưa
def is_already_marked(mssv):
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Bỏ qua dòng tiêu đề
            return any(row[0] == mssv for row in reader)
    except FileNotFoundError:
        return False

# Vòng lặp nhận diện và điểm danh
try:
    while True:
        ret, img = camera.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Kiểm tra nếu có khuôn mặt được phát hiện
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            roi_gray = gray[y:y + h, x:x + w]

            # Dự đoán ID và độ tin cậy của khuôn mặt
            label, confidence = model.predict(roi_gray)

            # Nếu độ tin cậy lớn hơn ngưỡng, đánh dấu là "Unknown"
            if confidence > confidence_threshold:
                label_text, mssv = "Unknown", None
            else:
                label_text, mssv = id_to_name_mssv.get(label, ("Unknown", None))

                # Kiểm tra nếu chưa điểm danh, thực hiện điểm danh
                if mssv and not is_already_marked(mssv):
                    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([mssv, label_text, 1])  # Ghi nhận điểm danh với giá trị 1
                    print(f"Đã điểm danh cho MSSV {mssv}")
                else:
                    print(f"MSSV {mssv} đã được điểm danh trước đó.")

            # Hiển thị thông tin nhận diện
            display_confidence = f"Confidence: {confidence:.2f}"
            color = (255, 0, 0) if label_text == "Unknown" else (0, 255, 0)
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            cv2.putText(img, display_confidence, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 1)

        cv2.imshow('Face Recognition', img)

        # Thoát khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Lỗi kết nối hoặc thực thi câu lệnh: {e}")

# Giải phóng tài nguyên
camera.release()
cv2.destroyAllWindows()
