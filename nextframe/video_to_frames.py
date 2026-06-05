import cv2
import os

def extract_frames_every_second(video_path, output_dir="extracted_frames"):
    # 저장할 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 '{output_dir}' 폴더를 생성했습니다.")

    # 영상 파일 열기
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ 영상을 열 수 없습니다. 경로를 확인해주세요.")
        return

    # 영상의 FPS(초당 프레임 수) 가져오기
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    print(f"🎬 영상 FPS: {fps} (1초에 {fps}프레임이 지나갑니다.)")

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # 영상이 끝나면 루프 탈출

        # 현재 프레임 번호가 FPS의 배수일 때만 저장 (즉, 1초마다 한 번)
        # 0초 시점의 프레임도 저장하고 싶다면 (frame_count % fps == 0)을 사용합니다.
        if frame_count > 0 and frame_count % fps == 0:
            saved_count += 1
            file_name = f"frame_{saved_count:03d}s.jpg"
            file_path = os.path.join(output_dir, file_name)
            
            # 이미지 파일로 저장
            cv2.imwrite(file_path, frame)
            print(f"💾 저장 완료: {file_path}")

        frame_count += 1

    cap.release()
    print(f"✨ 추출 종료! 총 {saved_count}개의 이미지가 '{output_dir}' 폴더에 저장되었습니다.")

# 💡 실행 구문 (현재 폴더의 car.mp4 기준)
if __name__ == "__main__":
    extract_frames_every_second("car.mp4")