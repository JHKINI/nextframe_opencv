# preprocess_v2.py (팀원 5 담당 - 통합 테스트용 전처리 함수화 버전)
import cv2

def apply_preprocessing(frame):
    """
    [통합 가이드]
    main.py의 동영상 루프 안에서 매 프레임(이미지 배열)을 받아와
    팀원 1의 전처리 알고리즘을 순차적으로 적용한 후,
    최종 결과물인 edge 이미지를 반환하는 함수입니다.
    """
    
    # 1. 컬러 영상을 흑백 영상으로 변환 (팀원 1 소스코드 적용)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. 가우시안 블러 적용 (팀원 1 소스코드 적용)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Edge Detection 적용 (팀원 1 소스코드 적용)
    edge = cv2.Canny(blur, 100, 200)
    
    # 다음 파이프라인(팀원 3의 번호판 영역 탐지)에서 사용할 수 있도록 
    # 최종 가공된 전처리 프레임(edge)을 반환(Return)합니다.
    return edge