#preprocess.py
import cv2
#영상파일불러오기
cap = cv2.VideoCapture("car.mp4")

while True:
    # 영상에서 한 프레임(사진 한 장) 읽기
    ret, frame = cap.read()
    if not ret:
        break
    # 원본 영상 출력
    cv2.imshow("video", frame)
    # 컬러 영상을 흑백 영상으로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 흑백 영상 출력
    cv2.imshow("gray",gray)
    #블러적용
    blur = cv2.GaussianBlur(gray, (5,5),0)
    cv2.imshow("blur",blur)
    #Edge Detection 적용
    edge = cv2.Canny(blur,100,200)

    cv2.imshow("edge",edge)
    # 30ms마다 키 입력 확인
    if cv2.waitKey(30) == 27:  # ESC 누르면 종료
        break
# 영상 객체 종료
cap.release()
# 모든 창 닫기
cv2.destroyAllWindows()