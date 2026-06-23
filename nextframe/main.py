# main.py (이진화 제거 - 방법 A 적용 통합본)
import sys
import cv2
import time
import os
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PIL import ImageFont, ImageDraw, Image
from collections import Counter

try:
    import preprocess_v2
except ImportError:
    preprocess_v2 = None

try:
    from detection import PlateDetector
    detector = PlateDetector()
except ImportError:
    detector = None

import ocr


# ==========================================================
# 🈶 한글 폰트 출력 헬퍼
# ==========================================================
FONT_PATH = os.path.join(os.path.dirname(__file__), "malgun.ttf")
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/malgun.ttf"


def put_text_kr(img, text, position, font_size=30, color=(0, 255, 0)):
    """OpenCV(BGR) 이미지에 한글을 그려서 BGR 이미지로 반환. color는 RGB 순서."""
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        font = ImageFont.load_default()
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


class LicensePlateApp(object):
    def __init__(self):
        loader = QUiLoader()
        ui_file_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        ui_file = QFile(ui_file_path)

        if not ui_file.open(QFile.ReadOnly):
            print(f"[파일 오류] '{ui_file_path}' 파일을 열 수 없습니다.")
            sys.exit(-1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if not self.window:
            print("[오류] UI 파일을 로드하는 데 실패했습니다.")
            sys.exit(-1)

        self.window.setWindowTitle("Next Frame - YOLO 딥러닝 번호판 인식 시스템 (통합 관제)")
        self.window.setFixedSize(1200, 750)

        self.btn_play = self.window.btn_play
        self.screen_main = self.window.screen_main
        self.screen_thresh = self.window.screen_thresh
        self.screen_crop = self.window.screen_crop

        self.video_filename = "car8.mp4"

        if not os.path.exists(self.video_filename):
            print(f"[경로 오류] '{self.video_filename}' 파일이 존재하지 않습니다.")
            print("💡 program/nextframe 폴더 안에 car8.mp4를 넣어주세요.")
            sys.exit()

        self.cap = cv2.VideoCapture(self.video_filename)
        print(f"[시스템] '{self.video_filename}' 동영상 파이프라인 가동을 시작합니다.")

        self.btn_play.clicked.connect(self.toggle_video)
        self.window.closeEvent = self.closeEvent

        # 🚀 [사이클 제어 및 베스트 컷 변수]
        self.is_tracking = False
        # ✅ [변경] (흑백패딩본, 컬러패딩본) 쌍으로 저장
        self.cycle_images = []
        self.last_license_number = "인식 대기 중"

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pipeline)
        self.timer.start(30)

    def show(self):
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
        delta = curr_time - self.prev_time
        fps = 0 if delta <= 0 else 1 / delta
        self.prev_time = curr_time

        # 2. 전처리 및 AI 탐지
        t0 = time.time()  # ⏱️ [측정] 시작

        if preprocess_v2 and hasattr(preprocess_v2, 'apply_preprocessing'):
            edge_frame = preprocess_v2.apply_preprocessing(frame)
        else:
            gray_feed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray_feed, (5, 5), 0)
            edge_frame = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        t1 = time.time()  # ⏱️ [측정] 전처리 끝

        if detector:
            display_frame, cropped_plate, cropped_plate_color = detector.detect_frame(frame, conf_thres=0.25)
        else:
            display_frame = frame.copy()
            cropped_plate = None
            cropped_plate_color = None

        t2 = time.time()  # ⏱️ [측정] YOLO 끝

        # FPS (영문/숫자 → 기존 putText)
        fps_text = f"FPS: {int(fps)}"
        cv2.putText(display_frame, fps_text, (display_frame.shape[1] - 150, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # OCR 텍스트 (한글 → PIL 헬퍼)
        ocr_text = f"OCR: {self.last_license_number}"
        display_frame = put_text_kr(display_frame, ocr_text, (30, 30),
                                    font_size=30, color=(0, 255, 0))

        t3 = time.time()  # ⏱️ [측정] 텍스트 그리기 끝

        start_time = time.time()
        execution_time = time.time() - start_time
        license_number = self.last_license_number

        # 3. UI 화면 출력
        self.display_image(display_frame, self.screen_main)
        self.display_image(edge_frame, self.screen_thresh)

        t4 = time.time()  # ⏱️ [측정] UI 출력 끝

        # ⏱️ [측정] 결과 출력 (총합 기준 FPS도 함께)
        #total = t4 - t0
        #print(f"[TIME] 전처리:{(t1-t0)*1000:5.0f}ms | "
        #      f"YOLO:{(t2-t1)*1000:5.0f}ms | "
        #      f"텍스트:{(t3-t2)*1000:5.0f}ms | "
        #      f"UI:{(t4-t3)*1000:5.0f}ms | "
        #      f"합계:{total*1000:5.0f}ms ({1/total if total>0 else 0:.1f} FPS)")

        # 4. 번호판 처리 로직
        if cropped_plate is not None:
            try:
                orig_h, orig_w = cropped_plate.shape[:2]
                padding_size = 15

                # 흑백본 패딩 (화면 표시·저장용)
                padded_plate = cv2.copyMakeBorder(cropped_plate, padding_size, padding_size,
                                                  padding_size, padding_size,
                                                  cv2.BORDER_CONSTANT, value=[255, 255, 255])

                # ✅ 컬러본 패딩 (OCR용) — 없을 수도 있으니 방어 처리
                if cropped_plate_color is not None:
                    padded_color = cv2.copyMakeBorder(cropped_plate_color, padding_size, padding_size,
                                                      padding_size, padding_size,
                                                      cv2.BORDER_CONSTANT, value=[255, 255, 255])
                else:
                    padded_color = None

                # 화면 표시는 기존대로 흑백
                self.display_image(padded_plate, self.screen_crop)

                if not self.is_tracking:
                    self.is_tracking = True
                    self.cycle_images = []
                    print("\n🎯 [TRACKING START] 새로운 차량 포착!")

                if orig_h > 0:
                    aspect_ratio = orig_w / orig_h
                    if 1.5 <= aspect_ratio <= 5.5:
                        # ✅ (흑백, 컬러) 쌍으로 저장
                        self.cycle_images.append((padded_plate, padded_color))
            except Exception as e:
                print(f"🚨 [프로세스 오류] {e}")

        else:
            if self.is_tracking:
                self.is_tracking = False
                print("🏁 [TRACKING END] 차량이 화면을 벗어났습니다.")

                if self.cycle_images:
                    save_dir = "saved_plates"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)

                    # 면적 상위 5장 선정 (흑백본 면적 기준)
                    candidates = sorted(
                        self.cycle_images,
                        key=lambda p: p[0].shape[0] * p[0].shape[1],
                        reverse=True
                    )[:5]

                    # 저장은 가장 큰 흑백본 1장 (기존과 동일)
                    best_bin, best_color = candidates[0]

                    timestamp = time.strftime("%Y%m%d_%H%M%S")

                    if best_color is not None:
                        file_path = os.path.join(save_dir, f"ocr_color_plate_{timestamp}.png")
                        cv2.imwrite(file_path, best_color)
                        print(f"✅ [OCR 컬러 저장 완료] 파일명: {file_path}")
                    else:
                        file_path = os.path.join(save_dir, f"ocr_fallback_bin_plate_{timestamp}.png")
                        cv2.imwrite(file_path, best_bin)
                        print(f"⚠️ [컬러본 없음 - 흑백 저장] 파일명: {file_path}")

                    # 후보 5장 OCR → 형식 통과한 것만 모으기
                    valid_results = []
                    for _bin, _color in candidates:
                        ocr_input = _color if _color is not None else _bin
                        r = ocr.read_plate(ocr_input)
                        if r:  # 형식 통과(빈 문자열 아님)한 것만
                            valid_results.append(r)

                    if valid_results:
                        # 가장 많이 나온 결과 채택 (투표)
                        best_result = Counter(valid_results).most_common(1)[0][0]
                        license_number = best_result
                        self.last_license_number = best_result
                        print(f"🔤 [OCR 투표 결과] {best_result} (후보: {valid_results})")
                    else:
                        print("🚫 [형식 불일치] 유효한 번호판을 찾지 못했습니다.")
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