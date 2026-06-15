# main.py (파편 컷 원천 차단 및 정상 비율 번호판 선별 저장 통합본)
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
    detector = PlateDetector() # YOLO 가중치 모델 초기화 인스턴스
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
        self.window.setWindowTitle("Next Frame - YOLO 딥러닝 번호판 인식 시스템 (통합 관제)")
        self.window.setFixedSize(1200, 750)
        
        # --------------------------------------------------
        # 🎯 2. UI 내 위젯 매핑 (Qt Designer의 objectName 기준)
        # --------------------------------------------------
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
        
        # 🚀 [사이클 제어 및 베스트 컷 변수] 
        self.is_tracking = False      # 현재 차량 번호판을 추적 중인지 여부
        self.cycle_images = []        # 이번 사이클 동안 검출된 모든 번호판 이미지를 임시 수집할 버퍼 리스트
        
        # 실시간 재생용 타이머 가동 (30ms 주기)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pipeline)
        self.timer.start(30)

    def show(self):
        """윈도우를 화면에 표시하는 메서드"""
        self.window.show()

    def update_pipeline(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # 1. FPS 계산
        if not hasattr(self, 'prev_time'):
            self.prev_time = time.time()
            
        curr_time = time.time()
        fps = 1 / (curr_time - self.prev_time)
        self.prev_time = curr_time
        
        # 2. 전처리 및 AI 탐지 (detector 호출 위치)
        if preprocess_v2 and hasattr(preprocess_v2, 'apply_preprocessing'):
            edge_frame = preprocess_v2.apply_preprocessing(frame)
        else:
            gray_feed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray_feed, (5, 5), 0)
            edge_frame = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        if detector:
            display_frame, cropped_plate = detector.detect_frame(frame, conf_thres=0.25)
        else:
            display_frame = frame.copy()
            cropped_plate = None 

        # 🚀 [수정 위치] display_frame이 정의된 직후에 텍스트를 작성합니다.
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(display_frame, fps_text, (display_frame.shape[1] - 150, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # 3. 실행 시간 및 기본 데이터 계산
        start_time = time.time() # 시간 측정은 루프 내에서 수행
        execution_time = time.time() - start_time
        license_number = "인식 모델 대기 중"

        # 3. UI 화면 출력
        self.display_image(display_frame, self.screen_main)
        self.display_image(edge_frame, self.screen_thresh)
        
        # 4. 번호판 처리 로직
        if cropped_plate is not None:
            try:
                orig_h, orig_w = cropped_plate.shape[:2]
                padding_size = 15
                padded_plate = cv2.copyMakeBorder(cropped_plate, padding_size, padding_size, padding_size, padding_size, 
                                                  cv2.BORDER_CONSTANT, value=[255, 255, 255])
                self.display_image(padded_plate, self.screen_crop)
                
                if not self.is_tracking:
                    self.is_tracking = True
                    self.cycle_images = [] 
                    print("\n🎯 [TRACKING START] 새로운 차량 포착!")
                
                if orig_h > 0:
                    aspect_ratio = orig_w / orig_h
                    if 1.5 <= aspect_ratio <= 5.5:
                        self.cycle_images.append(padded_plate)
            except Exception as e:
                print(f"🚨 [프로세스 오류] {e}")
                
        else:
            if self.is_tracking:
                self.is_tracking = False 
                print("🏁 [TRACKING END] 차량이 화면을 벗어났습니다.")
                
                # 저장 로직 구현
                if self.cycle_images:
                    # 면적(h*w)이 가장 큰 이미지 1장을 선정
                    best_plate = max(self.cycle_images, key=lambda img: img.shape[0] * img.shape[1])
                    
                    save_dir = "saved_plates"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    file_path = os.path.join(save_dir, f"best_plate_{timestamp}.png")
                    
                    cv2.imwrite(file_path, best_plate)
                    print(f"✅ [저장 완료] 파일명: {file_path}")
                else:
                    print("⚠️ [SYSTEM WARNING] 유효한 번호판 컷이 없어 저장하지 않았습니다.")
                
                print("================================================  \n")
            
            self.screen_crop.setText(f"🔍 추적 중... (RT: {execution_time:.3f}s)\nOCR: {license_number}")
            
  
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
    app_instance.show() 
    sys.exit(app.exec())