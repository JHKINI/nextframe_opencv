import cv2
import numpy as np
import os
from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path="best.pt"):
        print(f"DEBUG: 모델 경로 확인 -> {os.path.abspath(model_path)}") # 절대 경로 출력 2026-06-15
        self.model = YOLO(model_path)

    def detect_frame(self, frame, conf_thres=0.25):
        # 1. 모델 추론
        results = self.model(frame, imgsz=1088, verbose=False, iou=0.7, conf=conf_thres)[0]
        
        contour_img = frame.copy()
        cropped_plate_bin = None

        # 2. 탐지된 객체 수를 변수로 저장
        box_count = len(results.boxes)

        # 3. 객체가 탐지된 경우에만 로직 수행 및 출력
        if box_count > 0:
            # 탐지되었을 때만 출력
            print(f"객체 탐지 성공! (탐지된 객체 수: {box_count})")
            
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                
                # 탐지된 정보 출력
                print(f"Detected Class ID: {cls_id}, Confidence: {conf:.2f}")
                
                if cls_id == 0:  # 팀원 모델의 클래스 ID에 맞춰 수정하세요
                    # ... (박스 그리기 및 크롭 로직은 그대로 유지)
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
                    
                    cv2.rectangle(contour_img, (c_x1, c_y1), (c_x2, c_y2), (0, 255, 0), 2)
                    
                    label = f"Plate: {conf:.2f}"
                    (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                    cv2.rectangle(contour_img, (c_x1, c_y1 - text_height - 5), (c_x1 + text_width, c_y1), (0, 255, 0), -1)
                    cv2.putText(contour_img, label, (c_x1, c_y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
                    
                    vehicle_plate = frame[c_y1:c_y2, c_x1:c_x2]
                    if vehicle_plate.size > 0:
                        gray_plate = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
                        _, cropped_plate_bin = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    break # 단일 번호판 처리
                
        return contour_img, cropped_plate_bin