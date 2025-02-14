import subprocess
import tkinter as tk
from tkinter import font, filedialog
import cv2
import os

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giao diện Nhập Thông Tin")
root.geometry("800x600")
root.configure(bg="#EAEFF1")  # Màu nền nhẹ nhàng

# Font chữ chung cho nhãn và nút
label_font = font.Font(family="Arial", size=12, weight="bold")
button_font = font.Font(family="Arial", size=10)

# Tạo frame để chứa các thành phần nhập liệu với màu nền trắng và góc bo
frame = tk.Frame(root, bd=2, relief="flat", bg="white")
frame.place(x=150, y=100, width=500, height=180)

# Label và Textbox cho MSSV
label_mssv = tk.Label(frame, text="MSSV:", font=label_font, bg="white", fg="#333")
label_mssv.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_mssv = tk.Entry(frame, width=30, font=("Arial", 10))
entry_mssv.grid(row=0, column=1, padx=10, pady=10)

# Label và Textbox cho Họ và Tên
label_name = tk.Label(frame, text="Họ và Tên:", font=label_font, bg="white", fg="#333")
label_name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_name = tk.Entry(frame, width=30, font=("Arial", 10))
entry_name.grid(row=1, column=1, padx=10, pady=10)

# Label và Textbox cho Video
label_video = tk.Label(frame, text="Video:", font=label_font, bg="white", fg="#333")
label_video.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_video = tk.Entry(frame, width=30, font=("Arial", 10))
entry_video.grid(row=2, column=1, padx=10, pady=10)

# Tạo frame chứa các nút với màu nền nhẹ nhàng
button_frame = tk.Frame(root, bg="#EAEFF1")
button_frame.place(x=150, y=300, width=500, height=100)

# Label thông báo
label_thongbao = tk.Label(root, text="", font=label_font, bg="#EAEFF1", fg="#333")
label_thongbao.place(x=150, y=420)

# Hàm xử lý nhấn nút Lấy Ảnh
def layanh():
    mssv = entry_mssv.get()
    name = entry_name.get()

    # Kiểm tra xem MSSV đã tồn tại chưa
    id_name_mssv_file = 'id_name_mssv.txt'
    if os.path.exists(id_name_mssv_file):
        with open(id_name_mssv_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.split(',')[1] == mssv:  # Kiểm tra MSSV trong file
                    label_thongbao.config(text=f"MSSV '{mssv}' đã tồn tại!", fg="#f44336")
                    return

    # Gọi file Layanh.py và truyền name và mssv như tham số
    subprocess.run(["python", "Layanh.py", name, mssv])

    # Cập nhật label thông báo
    label_thongbao.config(text=f"MSSV: {mssv} - Họ và Tên: {name} đã thêm thành công", fg="#4CAF50")

def huanluyen():
    # Gọi file Huanluyenanh.py
    subprocess.run(["python", "Huanluyenanh.py"])
    label_thongbao.config(text=f"Huấn luyện hoàn tất và mô hình đã được lưu", fg="#4CAF50")


def diemdanh():
    # Gọi file Diemdanh.py
    subprocess.run(["python", "Diemdanh.py"])
    label_thongbao.config(text=f"Đã xuất file CSV", fg="#4CAF50")

def thoat():
    root.destroy()  # Đóng cửa sổ chính

def video_sang_anh():
    mssv = entry_mssv.get()
    name = entry_name.get()
    video = entry_video.get()

    # Kiểm tra xem MSSV đã tồn tại chưa
    id_name_mssv_file = 'id_name_mssv.txt'
    if os.path.exists(id_name_mssv_file):
        with open(id_name_mssv_file, 'r', encoding='utf-8') as file:
            for line in file:
                if line.split(',')[1] == mssv:  # Kiểm tra MSSV trong file
                    label_thongbao.config(text=f"MSSV '{mssv}' đã tồn tại!", fg="#f44336")
                    return

    # Tự động thêm đuôi .mp4 vào video
    video_with_extension = f"{video}.mp4"
    video_path = os.path.join("video", video_with_extension)

    # Kiểm tra xem video có tồn tại không
    if not os.path.exists(video_path):
        label_thongbao.config(text=f"Video '{video_with_extension}' không tồn tại!", fg="#f44336")
        return

    # Gọi file VideoToFrame.py và truyền name, mssv, và video với đuôi
    subprocess.run(["python", "VideoToFrame.py", name, mssv, video_with_extension])

    # Cập nhật label thông báo
    label_thongbao.config(text=f"MSSV: {mssv} - Họ và Tên: {name} đã thêm thành công", fg="#4CAF50")

# Kích thước của nút
button_width = 20
button_height = 2

# Tạo các nút với màu sắc hài hòa và cùng kích thước
btn_layanh = tk.Button(button_frame, text="Lấy Ảnh", width=button_width, height=button_height, font=button_font, bg="#4CAF50", fg="white", command=layanh)
btn_layanh.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

btn_huanluyen = tk.Button(button_frame, text="Huấn Luyện Ảnh", width=button_width, height=button_height, font=button_font, bg="#2196F3", fg="white", command=huanluyen)
btn_huanluyen.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

btn_diemdanh = tk.Button(button_frame, text="Điểm Danh", width=button_width, height=button_height, font=button_font, bg="#FF5722", fg="white", command=diemdanh)
btn_diemdanh.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

btn_video_to_image = tk.Button(button_frame, text="Chọn Video Sang Ảnh", width=button_width, height=button_height, font=button_font, bg="#FF9800", fg="white", command=video_sang_anh)
btn_video_to_image.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

btn_thoat = tk.Button(button_frame, text="Thoát", width=button_width, height=button_height, font=button_font, bg="#f44336", fg="white", command=thoat)
btn_thoat.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

# Cấu hình để tất cả các cột có kích thước bằng nhau
for i in range(5):
    button_frame.grid_columnconfigure(i, weight=1)

# Chạy ứng dụng
root.mainloop()