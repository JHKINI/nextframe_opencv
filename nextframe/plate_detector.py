# plate_detector.py
import sys
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap

# 💡 방금 위에서 분리한 기욱님의 탐지 모듈을 임포트합니다!
from detection import PlateDetector

class LicensePlateApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Next Frame - YOLOv11 딥러닝 번호판 검출 시스템")
        self.setFixedSize(1200, 750)
        
        # 💡 분리된 클래스를 선언하여 모델을 로드합니다.
        self.detector = PlateDetector("runs/detect/train-5/weights/best.pt") 
        
        self.video_path = "car.mp4"
        self.cap = cv2.VideoCapture(self.video_path)
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        
        self.btn_play.clicked.connect(self.toggle_video)
        
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        top_layout = QHBoxLayout()
        title_label = QLabel("🚗 YOLOv11 딥러닝 번호판 인식 시스템 (김기욱)")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.btn_play = QPushButton("일시정지")
        self.btn_play.setFixedWidth(100)
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.btn_play)
        main_layout.addLayout(top_layout)
        
        video_layout = QHBoxLayout()
        
        # 📺 1. 메인 화면 크기 고정
        self.screen_main = QLabel("영상을 불러오는 중...")
        self.screen_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_main.setStyleSheet("border: 2px solid #333; background-color: black;")
        self.screen_main.setMinimumSize(770, 550)
        self.screen_main.setMaximumSize(770, 550)
        
        side_layout = QVBoxLayout()
        
        # ⚙️ 2. AI 분석 피드 크기 고정
        self.screen_thresh = QLabel("AI 분석 피드")
        self.screen_thresh.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_thresh.setStyleSheet("border: 1px solid #664455; background-color: black;")
        self.screen_thresh.setMinimumSize(330, 270)
        self.screen_thresh.setMaximumSize(330, 270)
        
        # 🔍 3. 크롭된 번호판 패치 크기 고정
        self.screen_crop = QLabel("인식된 번호판 (OCR 연계)")
        self.screen_crop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen_crop.setStyleSheet("border: 2px solid green; background-color: #222; color: white; font-weight: bold;")
        self.screen_crop.setMinimumSize(330, 220)
        self.screen_crop.setMaximumSize(330, 220)
        
        side_layout.addWidget(QLabel("⚙️ YOLOv11 Gray 피드"))
        side_layout.addWidget(self.screen_thresh)
        side_layout.addWidget(QLabel("🔍 크롭된 번호판 패치"))
        side_layout.addWidget(self.screen_crop)
        
        video_layout.addWidget(self.screen_main)
        video_layout.addLayout(side_layout)
        main_layout.addLayout(video_layout)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # ==========================================================
        # 🧠 [기욱님의 분리된 추론 모듈 호출]
        # ==========================================================
        # 원본 프레임을 던져주면, 수정한 detection.py가 알아서 박스를 그리고 크롭까지 해서 반환합니다.
        contour_img, cropped_plate_bin = self.detector.detect_frame(frame, conf_thres=0.45)

        # 📺 메인 화면 갱신
        self.display_image(contour_img, self.screen_main)
        
        # 팀원의 전처리(Adaptive Threshold) 구현부 반영
        gray_feed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray_feed, (5, 5), 0)
        thresh_feed = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        self.display_image(thresh_feed, self.screen_thresh, is_gray=True)
        
        # 번호판 크롭 이미지 출력
        if cropped_plate_bin is not None:
            self.display_image(cropped_plate_bin, self.screen_crop, is_gray=True)
        else:
            self.screen_crop.setText("🔍 번호판 추적 중...")

    def display_image(self, ocv_img, target_label, is_gray=False):
        if is_gray:
            h, w = ocv_img.shape
            bytes_per_line = w
            q_img = QImage(ocv_img.data, w, h, bytes_per_line, QImage.Format.Format_Grayscale8)
        else:
            h, w, ch = ocv_img.shape
            bytes_per_line = ch * w
            rgb_img = cv2.cvtColor(ocv_img, cv2.COLOR_BGR2RGB)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LicensePlateApp()
    window.show()
    sys.exit(app.exec())