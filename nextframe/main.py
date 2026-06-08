# main.py (QUiLoader 하얀 화면 버그 수정 완료본)
import sys
import cv2
import time
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, Qt
from PySide6.QtGui import QImage, QPixmap

# [통합 단계] 통합 테스트용 전처리 v2 모듈 가져오기
try:
    import preprocess_v2
except ImportError:
    preprocess_v2 = None

# ==========================================================
# 🚀 [기욱님 파트 연동] 
# ==========================================================
try:
    from detection import PlateDetector
    detector = PlateDetector() # YOLOv11 모델 초기화 인스턴스
except ImportError:
    detector = None

# [미래 통합 영역] 팀원 4가 OCR 파일을 완성하면 아래 주석(#)을 해제할 예정입니다.
# import ocr


class LicensePlateApp(object): # QMainWindow 상속을 제거하여 꼬임 방지
    def __init__(self):
        # --------------------------------------------------
        # 📂 1. QUiLoader를 사용하여 ui 파일 동적 로드
        # --------------------------------------------------
        loader = QUiLoader()
        ui_file_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"[파일 오류] '{ui_file_path}' 파일을 열 수 없습니다.")
            sys.exit(-1)
            
        # UI 파일 자체를 메인 윈도우 객체로 로드합니다.
        self.window = loader.load(ui_file)
        ui_file.close()
        
        if not self.window:
            print("[오류] UI 파일을 로드하는 데 실패했습니다.")
            sys.exit(-1)
            
        # 기본 윈도우 속성 세팅
        self.window.setWindowTitle("Next Frame - YOLOv26 딥러닝 번호판 인식 시스템 (통합 관제)")
        self.window.setFixedSize(1200, 750)
        
        # --------------------------------------------------
        # 🎯 2. UI 내 위젯 매핑 (Qt Designer의 objectName 기준)
        # --------------------------------------------------
        # self.window 변수를 통해 위젯에 접근합니다.
        self.btn_play = self.window.btn_play
        self.screen_main = self.window.screen_main
        self.screen_thresh = self.window.screen_thresh
        self.screen_crop = self.window.screen_crop
        
        # --------------------------------------------------
        # 🎥 3. 비디오 소스 및 파이프라인 가동 설정
        # --------------------------------------------------
        self.video_filename = "car.mp4"
        
        if not os.path.exists(self.video_filename):
            print(f"[경로 오류] '{self.video_filename}' 파일이 존재하지 않습니다.")
            print("💡 program/nextframe 폴더 안에 car.mp4를 넣어주세요.")
            sys.exit()

        self.cap = cv2.VideoCapture(self.video_filename)
        print(f"[시스템] '{self.video_filename}' 동영상 파이프라인 가동을 시작합니다.")
        
        # 이벤트 및 타이머 연결
        self.btn_play.clicked.connect(self.toggle_video)
        self.window.closeEvent = self.closeEvent # 종료 이벤트 오버라이딩 대신 연결
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pipeline)
        self.timer.start(30)

    def show(self):
        """윈도우를 화면에 표시하는 메서드"""
        self.window.show()

    def update_pipeline(self):
        ret, frame = self.cap.read()
        if not ret:
            print("[시스템] 동영상 재생이 완료되었거나 프레임을 읽을 수 없습니다.")
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) # 무한 반복 재생 처리
            return
            
        start_time = time.time()
        
        # --------------------------------------------------
        # 2. [연동 완료] 팀원 1의 로직이 담긴 v2 전처리 함수 호출
        # --------------------------------------------------
        if preprocess_v2 and hasattr(preprocess_v2, 'apply_preprocessing'):
            edge_frame = preprocess_v2.apply_preprocessing(frame)
        else:
            gray_feed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray_feed, (5, 5), 0)
            edge_frame = cv2.adaptiveThreshold(
                blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )

        # --------------------------------------------------
        # 3. [연동 완료] 팀원 3(기욱님) 번호판 후보 영역 탐지 및 Crop
        # --------------------------------------------------
        if detector:
            display_frame, cropped_plate = detector.detect_frame(frame, conf_thres=0.25)
        else:
            display_frame = frame.copy()
            cropped_plate = None 

        # --------------------------------------------------
        # 4. [미래 연동 영역] 팀원 4 OCR 글자 인식 및 문자열 반환
        # --------------------------------------------------
        license_number = "인식 모델 대기 중"

        # --------------------------------------------------
        # 5. [시연 및 결과 출력] UI 화면에 실시간 매핑
        # --------------------------------------------------
        self.display_image(display_frame, self.screen_main)
        self.display_image(edge_frame, self.screen_thresh)
        
        if cropped_plate is not None:
            self.display_image(cropped_plate, self.screen_crop)
        else:
            self.screen_crop.setText(f"🔍 추적 중...\nOCR: {license_number}")
            
        execution_time = time.time() - start_time

    def display_image(self, ocv_img, target_label):
        if ocv_img is None or target_label is None:
            return
            
        img_copy = ocv_img.copy()
        shape_info = img_copy.shape
        
        if len(shape_info) == 2:
            h, w = shape_info
            bytes_per_line = w
            q_img = QImage(img_copy.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:
            h, w, ch = shape_info
            bytes_per_line = ch * w
            rgb_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)
            q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
        pixmap = QPixmap.fromImage(q_img)
        scaled_pixmap = pixmap.scaled(target_label.width(), target_label.height(), 
                                      Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        target_label.setPixmap(scaled_pixmap)

    def toggle_video(self):
        if self.timer.isActive(): 
            self.timer.stop()
            self.btn_play.setText("재생")
        else: 
            self.timer.start(30)
            self.btn_play.setText("일시정지")
            
    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        print("==================================================")
        print("[시스템] 파이프라인 관제 프로그램이 안전하게 종료되었습니다.")
        print("==================================================")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_instance = LicensePlateApp()
    app_instance.show() # 로드된 인스턴스 띄우기
    sys.exit(app.exec())