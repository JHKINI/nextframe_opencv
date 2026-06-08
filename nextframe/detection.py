# detection.py
import cv2
from ultralytics import YOLO

class PlateDetector:
    def __init__(self, model_path="best.pt"):
        """
        YOLOv26 가중치 모델을 초기화합니다.
        """
        self.model = YOLO(model_path)

    def detect_frame(self, frame, conf_thres=0.25):
        """
        프레임을 입력받아 번호판을 탐지하고 시각화 및 크롭을 수행합니다.
        """
        # 🪄 [핵심 해결책]: iou=0.45를 주어 겹쳐 나오는 중복 사각형들을 AI 단계에서 원천 차단(NMS)합니다.
        results = self.model(frame, verbose=False, iou=0.7)[0]
        contour_img = frame.copy()
        cropped_plate_bin = None

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            # 클래스 ID 0번(번호판) 필터링 조건
            if cls_id == 0 and conf > conf_thres:  
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 시각화 바운딩 박스 그리기 (초록색)
                cv2.rectangle(contour_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(contour_img, f"Plate {conf:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # 정밀 크롭
                vehicle_plate = frame[y1:y2, x1:x2]
                
                if vehicle_plate.size > 0:
                    gray_plate = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
                    _, cropped_plate_bin = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # 단 하나의 최고 확률 박스만 처리하고 탈출하여 중복 렌더링을 막습니다.
                break
                
        return contour_img, cropped_plate_bin