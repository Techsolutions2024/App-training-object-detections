
# App-training-object-detections 🖼️🤖

Ứng dụng này cung cấp công cụ và giao diện để **huấn luyện (training)** và **chạy inference** các mô hình **YOLO** thông qua **ONNX Runtime**.  
Mục tiêu là giúp người dùng dễ dàng thiết lập, huấn luyện, và triển khai mô hình nhận diện vật thể mà không cần nhiều thao tác phức tạp.

---

## 📂 Cấu trúc repo

```
App-training-object-detections/
│── YOLOTrainingStudio_v1.0.0_Portable/   # Phiên bản portable của ứng dụng
│── build/                                # Thư mục build
│── dist/                                 # Thư mục phân phối
│── app training 1.png                    # Ảnh minh họa giao diện
│── BUILD_README.md                       # Hướng dẫn build
│── QUICK_START.txt                       # Hướng dẫn nhanh
│── YOLOTrainingStudio.spec               # File cấu hình build
│── YOLOTrainingStudio_v1.0.0_Portable.zip# Bản portable nén
│── app_icon.ico                          # Icon ứng dụng
│── build.py                              # Script build
│── create_icon.py                        # Script tạo icon
│── installer_script.iss                  # Script tạo installer
│── main.py                               # Entry point ứng dụng
│── quick_build.bat                       # Batch build nhanh
│── requirements.txt                      # Thư viện cần thiết
│── version_info.txt                      # Thông tin version
│── yolo_trainer_gui.py                   # Giao diện huấn luyện YOLO
```

---

## ⚙️ Cài đặt

1. Clone repo:
   ```bash
   git clone https://github.com/Techsolutions2024/App-training-object-detections.git
   cd App-training-object-detections
   ```

2. Cài đặt dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy ứng dụng:
   ```bash
   python main.py
   ```

---

## 🚀 Tính năng chính

- Giao diện trực quan để **huấn luyện YOLO models**.  
- Hỗ trợ **ONNX Runtime inference**.  
- Tích hợp công cụ build để tạo bản portable hoặc installer.  
- Hỗ trợ quản lý phiên bản và cấu hình nhanh.  
- Xuất kết quả huấn luyện/inference trực tiếp từ ứng dụng.  

---

## 📖 Hướng dẫn nhanh

- Mở ứng dụng qua `main.py` hoặc bản portable.  
- Chọn mô hình YOLO (ONNX).  
- Chọn dataset để huấn luyện.  
- Theo dõi tiến trình training qua giao diện.  
- Chạy inference trực tiếp trên ảnh/video.  

---

## 🧩 Hướng phát triển

- Thêm hỗ trợ nhiều phiên bản YOLO (YOLOv5, YOLOv8, YOLOv11).  
- Tích hợp lựa chọn CPU/GPU trong giao diện.  
- Thêm module quản lý dataset.  
- Xuất báo cáo training chi tiết.  

---

## 📜 License

MIT License – bạn có thể sử dụng, chỉnh sửa và phát triển repo này cho mục đích cá nhân hoặc thương mại.
