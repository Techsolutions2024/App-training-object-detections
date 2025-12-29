from ultralytics import YOLO

def main():
    # 1. Khởi tạo mô hình
    # Bạn có thể dùng 'yolov8n.pt' (Nano) hoặc 'yolov8s.pt' (Small) tùy cấu hình máy
    model = YOLO("yolo11s.pt")

    # 2. Huấn luyện mô hình
    # device=0 sẽ chỉ định chạy trên GPU đầu tiên. 
    # Nếu không có GPU, nó sẽ tự động chuyển sang CPU.
    rresults = model.train(
    data="helmat.v1i.yolov11/data.yaml",
    epochs=100,
    imgsz=768,
    batch=8,
    device=0,
    workers=4,

    optimizer="AdamW",
    lr0=0.004,
    lrf=0.01,
    cos_lr=True,
    weight_decay=0.0005,

    warmup_epochs=5,

    hsv_h=0.02,
    hsv_s=0.7,
    hsv_v=0.5,
    mosaic=1.0,
    close_mosaic=20,
    mixup=0.15,
    copy_paste=0.3,

    conf=0.001,
    iou=0.7,

    patience=50,
    amp=True,
    pretrained=True,
    plots=True
)

if __name__ == "__main__":
    main()