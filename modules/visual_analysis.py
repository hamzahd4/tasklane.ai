from ultralytics import YOLO
from paddleocr import PaddleOCR

model = YOLO("yolov8n.pt")
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def analyze_frame(image_path):
    yolo_results = model(image_path)
    
    yolo_data = []
    for result in yolo_results:
        if result.boxes is not None:
            for box in result.boxes:
                yolo_data.append({
                    "class": model.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "bbox": box.xyxy.tolist(),
                })

    ocr_output = ocr.ocr(image_path)
    ocr_data = []
    if ocr_output:
        for block in ocr_output:
            for line in block:
                if len(line) > 1:
                    text = line[1][0]
                    ocr_data.append(text)

    return yolo_data, ocr_data
