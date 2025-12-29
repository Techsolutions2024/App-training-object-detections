# YOLO Training Studio - Build Instructions

## 📦 Publisher: TxTech

## Yêu Cầu Hệ Thống

### Để Build Phần Mềm:
1. **Python 3.8+** đã cài đặt
2. **PyInstaller**: `pip install pyinstaller`
3. **Pillow** (tùy chọn, để tạo icon): `pip install pillow`
4. **Inno Setup** (để tạo installer): [Download tại đây](https://jrsoftware.org/isdl.php)

### Để Chạy Phần Mềm:
- Python 3.8 trở lên
- Các thư viện trong `requirements.txt`

## 🚀 Cách Build

### Build Tất Cả (Khuyến Nghị)
```bash
python build.py all
```
Lệnh này sẽ tạo:
- ✅ File executable (.exe)
- ✅ Installer (.exe với Inno Setup)
- ✅ Portable ZIP package

### Build Từng Phần

#### 1. Chỉ Build Executable
```bash
python build.py exe
```
Kết quả: `dist/YOLOTrainingStudio.exe`

#### 2. Chỉ Build Installer
```bash
python build.py installer
```
Kết quả: `installer/YOLOTrainingStudio_Setup_v1.0.0.exe`

**Lưu ý**: Cần cài đặt Inno Setup trước

#### 3. Chỉ Build Portable ZIP
```bash
python build.py portable
```
Kết quả: `YOLOTrainingStudio_v1.0.0_Portable.zip`

#### 4. Dọn Dẹp Build Files
```bash
python build.py clean
```

## 📁 Cấu Trúc Sau Khi Build

```
vision/
├── build.py                          # Build script
├── yolo_trainer_gui.py              # Source code chính
├── requirements.txt                  # Dependencies
├── app_icon.ico                     # Icon (tự động tạo)
├── dist/
│   └── YOLOTrainingStudio.exe      # Executable
├── installer/
│   └── YOLOTrainingStudio_Setup_v1.0.0.exe  # Installer
└── YOLOTrainingStudio_v1.0.0_Portable.zip   # Portable package
```

## 🔧 Tùy Chỉnh Build

### Thay Đổi Thông Tin Phần Mềm
Mở `build.py` và chỉnh sửa:

```python
APP_NAME = "YOLO Training Studio"
APP_VERSION = "1.0.0"
PUBLISHER = "TxTech"
```

### Thêm Icon Tùy Chỉnh
1. Tạo file icon `app_icon.ico` (256x256 pixels)
2. Đặt trong thư mục gốc cùng với `build.py`
3. Build lại

### Thêm Files Vào Package
Trong `build.py`, tìm phần `args.extend([...])` và thêm:

```python
args.extend([
    '--add-data=your_file.txt;.',
    '--add-data=your_folder;your_folder',
])
```

## 📋 Chi Tiết Build Process

### 1. PyInstaller
- Đóng gói Python code thành executable
- Bao gồm tất cả dependencies
- Single file mode (--onefile)
- Windowed mode (không hiện console)

### 2. Inno Setup
- Tạo installer chuyên nghiệp
- Hỗ trợ nhiều ngôn ngữ (English, Vietnamese)
- Tự động tạo shortcuts
- Kiểm tra Python installation
- Tùy chọn cài đặt dependencies

### 3. Portable Package
- Không cần cài đặt
- Chạy trực tiếp từ USB/folder
- Bao gồm README và requirements.txt

## ⚠️ Xử Lý Lỗi Thường Gặp

### Lỗi: "PyInstaller not found"
```bash
pip install pyinstaller
```

### Lỗi: "Inno Setup not found"
- Download và cài đặt Inno Setup từ: https://jrsoftware.org/isdl.php
- Hoặc chỉ build executable: `python build.py exe`

### Lỗi: "Failed to execute script"
- Kiểm tra tất cả dependencies đã được cài đặt
- Thử build lại với `python build.py clean` trước

### Lỗi: "Icon creation failed"
```bash
pip install pillow
```

## 🎯 Phân Phối Phần Mềm

### Installer (Khuyến Nghị cho End Users)
- File: `installer/YOLOTrainingStudio_Setup_v1.0.0.exe`
- Ưu điểm:
  - Cài đặt chuyên nghiệp
  - Tự động tạo shortcuts
  - Dễ gỡ cài đặt
  - Kiểm tra dependencies

### Portable (Cho Advanced Users)
- File: `YOLOTrainingStudio_v1.0.0_Portable.zip`
- Ưu điểm:
  - Không cần cài đặt
  - Chạy từ bất kỳ đâu
  - Dễ backup và di chuyển

### Standalone Executable
- File: `dist/YOLOTrainingStudio.exe`
- Ưu điểm:
  - Single file
  - Chạy ngay lập tức
  - Nhỏ gọn nhất

## 📝 Release Checklist

Trước khi phát hành phiên bản mới:

- [ ] Cập nhật `APP_VERSION` trong `build.py`
- [ ] Test phần mềm trên máy sạch (không có Python)
- [ ] Kiểm tra tất cả tính năng hoạt động
- [ ] Build với `python build.py all`
- [ ] Test installer trên máy sạch
- [ ] Tạo release notes
- [ ] Upload lên website/repository

## 🔐 Code Signing (Tùy Chọn)

Để ký số phần mềm (tránh Windows SmartScreen warning):

1. Mua code signing certificate
2. Thêm vào PyInstaller:
```python
args.extend([
    '--sign',
    '--sign-options=your_certificate.pfx',
])
```

## 📞 Hỗ Trợ

- **Publisher**: TxTech
- **Website**: https://txtech.com
- **Email**: support@txtech.com

## 📄 License

© 2025 TxTech - All Rights Reserved

---

**Chúc bạn build thành công! 🎉**
