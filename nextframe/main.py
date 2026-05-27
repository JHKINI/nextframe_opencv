# main.py (팀원 5 담당 - 전체 기능 연결 및 시연 모듈)
import cv2
import time
import os

# [통합 단계] 통합 테스트용 전처리 v2 모듈 가져오기
try:
    import preprocess_v2
except ImportError:
    preprocess_v2 = None

# [미래 통합 영역] 팀원 3, 4가 파일을 완성하면 아래 주석(#)을 해제할 예정입니다.
# import detection
# import ocr

def main():
    print("==================================================")
    print("[시스템] Next Frame 차량 번호판 인식 파이프라인 가동")
    print("==================================================")
    
    # 1. 파일 경로 설정 (program/nextframe 폴더 기준)
    video_filename = "car.mp4"
    
    # QA 작업: 파일이 현재 폴더에 진짜 존재하는지 선제적 체크 (팀원 5 업무)
    if not os.path.exists(video_filename):
        print(f"[경로 오류] '{video_filename}' 파일이 존재하지 않습니다.")
        print(f"현재 작업 디렉토리: {os.getcwd()}")
        print("💡 바탕화면/팀 프로젝트/program/nextframe 폴더 안에 car.mp4를 넣어주세요.")
        return

    cap = cv2.VideoCapture(video_filename)
    print(f"[시스템] '{video_filename}' 동영상 스트리밍을 시작합니다.")
    print(" -> 시연 종료 방법: 영상 화면을 클릭한 후 키보드의 'ESC' 키 입력\n")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[시스템] 동영상 재생이 완료되었거나 프레임을 읽을 수 없습니다.")
            break
            
        # 성능 평가(QA)를 위한 프레임별 처리 시간 측정 시작 (팀원 5 업무)
        start_time = time.time()
        
        # --------------------------------------------------
        # 2. [연동 완료] 팀원 1의 로직이 담긴 v2 전처리 함수 호출
        # --------------------------------------------------
        if preprocess_v2 and hasattr(preprocess_v2, 'apply_preprocessing'):
            # 원본 프레임(frame)을 던져서 흑백/블러/엣지가 처리된 이미지(edge_frame)를 받아옴
            edge_frame = preprocess_v2.apply_preprocessing(frame)
        else:
            # v2 파일이 없거나 매칭이 안 될 경우 에러 방지용 임시 처리
            edge_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        # --------------------------------------------------
        # 3. [미래 연동 영역] 팀원 3 번호판 후보 영역 탐지 및 Crop
        # --------------------------------------------------
        # cropped_plate = detection.find_plate(edge_frame)
        # 임시 대기 상태 코드 (팀원 3이 코드를 주면 위 주석을 풀고 아래를 대체합니다)
        cropped_plate = edge_frame 

        # --------------------------------------------------
        # 4. [미래 연동 영역] 팀원 4 OCR 글자 인식 및 문자열 반환
        # --------------------------------------------------
        # license_number = ocr.read_plate(cropped_plate)
        # 임시 대기 상태 코드 (팀원 4가 코드를 주면 위 주석을 풀고 아래를 대체합니다)
        license_number = "인식 모델 대기 중"

        # --------------------------------------------------
        # 5. [시연 및 결과 출력] 팀원 5 담당 메인 업무
        # --------------------------------------------------
        # 모니터링 창 띄우기 (원본 영상과 전처리된 윤곽선 영상을 동시에 대조 시연)
        cv2.imshow("Original Video (Input)", frame)
        cv2.imshow("Preprocessed Video (Canny Edge)", edge_frame)
        
        # 중간 발표 양식에 약속된 연산 시간 계산 로직 미리 구현
        execution_time = time.time() - start_time
        
        # 실시간 디버깅용 QA 로그 출력 (필요 시 주석 해제하여 사용)
        # print(f"[QA 분석] 차량번호: {license_number} | 처리속도: {execution_time:.4f}초")
        
        # 팀원 1의 기존 규칙 준수: 키보드의 ESC(아스키코드 27)를 누르면 시연 프로그램 종료
        if cv2.waitKey(30) == 27:
            print("[시스템] 사용자의 요청에 의해 시연이 중단되었습니다.")
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("==================================================")
    print("[시스템] 파이프라인 관제 프로그램이 안전하게 종료되었습니다.")
    print("==================================================")

if __name__ == "__main__":
    main()