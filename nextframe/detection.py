import cv2
import numpy as np
from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path="best.pt"):
        self.model = YOLO(model_path)

    def detect_frame(self, frame, conf_thres=0.25):
        # conf_thres를 적용하여 탐지 수행
        results = self.model(frame, verbose=False, iou=0.7, conf=conf_thres)[0]
        contour_img = frame.copy()
        cropped_plate_bin = None

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            if cls_id == 0:  
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 🪄 [동적 여백 계산]
                plate_w = x2 - x1
                plate_h = y2 - y1
                pad_x = int(plate_w * 0.1)
                pad_y = int(plate_h * 0.2)
                
                c_x1 = max(0, x1 - pad_x)
                c_y1 = max(0, y1 - pad_y)
                c_x2 = min(frame.shape[1], x2 + pad_x)
                c_y2 = min(frame.shape[0], y2 + pad_y)
                
                # 1. 시각화 박스 그리기
                cv2.rectangle(contour_img, (c_x1, c_y1), (c_x2, c_y2), (0, 255, 0), 2)
                
                # 2. 🪄 [추가] Confidence Score 텍스트 출력 로직
                label = f"Plate: {conf:.2f}"
                # 텍스트 크기 계산
                (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                # 텍스트 배경 박스 (가독성 향상)
                cv2.rectangle(contour_img, (c_x1, c_y1 - text_height - 5), (c_x1 + text_width, c_y1), (0, 255, 0), -1)
                # 텍스트 그리기
                cv2.putText(contour_img, label, (c_x1, c_y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                
                # 정밀 크롭
                vehicle_plate = frame[c_y1:c_y2, c_x1:c_x2]
                
                if vehicle_plate.size > 0:
                    gray_plate = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
                    _, cropped_plate_bin = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                break # 단일 번호판 처리
                
        return contour_img, cropped_plate_bin