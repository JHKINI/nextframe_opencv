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
                
                # 🪄 [핵심 해결책] 동적 여백 계산: 
                # 번호판의 가로(w), 세로(h) 크기에 비례해 여백을 줌
                plate_w = x2 - x1
                plate_h = y2 - y1
                
                # 가로/세로 비율에 맞춰 여백을 유연하게 늘림
                # 2줄 번호판(두꺼운 번호판)은 세로(h)가 길므로 상하 여백을 넉넉히 확보
                pad_x = int(plate_w * 0.1) # 좌우 10%
                pad_y = int(plate_h * 0.2) # 상하 20% (두꺼운 번호판 대응)
                
                # 이미지 범위를 넘지 않도록 제한
                c_x1 = max(0, x1 - pad_x)
                c_y1 = max(0, y1 - pad_y)
                c_x2 = min(frame.shape[1], x2 + pad_x)
                c_y2 = min(frame.shape[0], y2 + pad_y)
                
                # 시각화 박스 그리기
                cv2.rectangle(contour_img, (c_x1, c_y1), (c_x2, c_y2), (0, 255, 0), 2)
                
                # 정밀 크롭
                vehicle_plate = frame[c_y1:c_y2, c_x1:c_x2]
                
                if vehicle_plate.size > 0:
                    gray_plate = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
                    # Otsu 알고리즘으로 이진화
                    _, cropped_plate_bin = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                break # 단일 번호판 처리
                
        return contour_img, cropped_plate_bin