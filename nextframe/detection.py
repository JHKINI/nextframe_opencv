import cv2
from ultralytics import YOLO

class PlateDetector:
    # 💡 기본 가중치 경로를 runs 폴더 내부의 train-5 진짜 위치로 수정했습니다!
    def __init__(self, model_path="runs/detect/train-5/weights/best.pt"):
        """
        YOLOv11 가중치 모델을 초기화합니다.
        (기욱님이 고도화한 150 에포크 뻥튀기 모델 경로를 지정)
        """
        self.model = YOLO(model_path)

    def detect_frame(self, frame, conf_thres=0.45):
        """
        프레임을 입력받아 번호판을 탐지하고 시각화 및 크롭을 수행합니다.
        """
        results = self.model(frame, verbose=False)[0]
        contour_img = frame.copy()
        cropped_plate_bin = None

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            
            if cls_id == 0 and conf > conf_thres:  
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 📺 메인 화면 사각형 및 텍스트 시각화
                cv2.rectangle(contour_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(contour_img, f"Plate {conf:.2f}", (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # 🔍 번호판 영역 다이렉트 크롭
                vehicle_plate = frame[y1:y2, x1:x2]
                
                if vehicle_plate.size > 0:
                    plate_gray = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
                    _, cropped_plate_bin = cv2.threshold(
                        plate_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
                    )

        return contour_img, cropped_plate_bin