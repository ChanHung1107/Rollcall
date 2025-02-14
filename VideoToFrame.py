import sys
import os
import cv2


# Hàm chính để lấy khuôn mặt từ video
def extract_faces_from_video(video, mssv, name):
    video_directory = 'Video'
    video_path = os.path.join(video_directory, video)

    # Kiểm tra video có tồn tại
    if not os.path.exists(video_path):
        print(f"Không tìm thấy video '{video}' trong thư mục '{video_directory}'. Đường dẫn: {video_path}")
        return

    id_name_mssv_file = 'id_name_mssv.txt'

    # Tăng ID
    face_id = 0
    if os.path.exists(id_name_mssv_file):
        with open(id_name_mssv_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines:
                last_entry = lines[-1]
                last_id = int(last_entry.split(',')[0])
                face_id = last_id + 1

    data_directory = 'data'
    subdirectory = os.path.join(data_directory, f"face_{face_id}")
    os.makedirs(subdirectory, exist_ok=True)

    face_cascade_path = 'haarcascade_frontalface_default.xml'
    if not os.path.exists(face_cascade_path):
        print(f"Haar cascade file không tồn tại tại: {face_cascade_path}")
        return

    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    target_face_count = 300
    face_count = 0
    min_face_size = 66

    while face_count < target_face_count:
        cap = cv2.VideoCapture(video_path)

        # Kiểm tra xem video có mở được không
        if not cap.isOpened():
            print(f"Không thể mở video: {video_path}")
            return

        print("Bắt đầu xử lý video...")

        while face_count < target_face_count:
            ret, frame = cap.read()
            if not ret:  # Nếu video đã kết thúc
                print("Video đã kết thúc, bắt đầu lại...")
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video về đầu
                continue  # Tiếp tục vòng lặp để đọc lại video

            # Phát hiện khuôn mặt trong khung hình màu
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                if w < min_face_size or h < min_face_size:
                    continue  # Bỏ qua những khuôn mặt quá nhỏ

                face_color = frame[y:y + h, x:x + w]
                face_gray = cv2.cvtColor(face_color, cv2.COLOR_BGR2GRAY)
                face_count += 1

                face_filename = os.path.join(subdirectory, f"face_{face_count}.jpg")
                cv2.imwrite(face_filename, face_gray)
                print(f"Lưu khuôn mặt {face_count}: {face_filename}")

                if face_count >= target_face_count:
                    break  # Dừng nếu đã đủ số lượng khuôn mặt

        cap.release()  # Giải phóng tài nguyên video

    cv2.destroyAllWindows()

    with open(id_name_mssv_file, 'a', encoding='utf-8') as file:
        file.write(f"{face_id},{name},{mssv}\n")

    print(f"Đã lưu {face_count} khuôn mặt từ video '{video}' vào thư mục {subdirectory}.")
    print(f"Thông tin đã được lưu vào {id_name_mssv_file}: ID: {face_id}, Name: {name}, MSSV: {mssv}")


if __name__ == "__main__":
    # Đọc tham số từ dòng lệnh
    if len(sys.argv) != 4:
        print("Sử dụng: python VideoToFrame.py <name> <mssv> <video_filename>")
        sys.exit(1)

    name = sys.argv[1]
    mssv = sys.argv[2]
    video_filename = sys.argv[3]

    # Gọi hàm xử lý video
    extract_faces_from_video(video_filename, mssv, name)
