import os
from ultralytics import YOLO

def main():
    # 1. 기본 사전 학습 모델(yolo11n.pt) 로드
    model = YOLO("yolo11n.pt")

    # 2. 이동시킨 YOLODataset 폴더의 dataset.yaml 경로 설정
    yaml_path = "./YOLODataset/dataset.yaml"

    print("🚀 YOLOv11 커스텀 번호판 데이터 뻥튀기 및 재학습을 시작합니다...")
    
    # 3. YOLOv11 공식 인자명에 맞춘 실시간 데이터 증강 학습
    model.train(
        data=yaml_path,
        epochs=150,        # 150번 복습하며 매번 다른 형태의 변형 문제를 풀게 합니다.
        imgsz=640,         # 입력 이미지 크기
        batch=8,           # 배치 사이즈
        workers=2,         # 데이터 로드 프로세스 수
        device=0,          # GPU 사용 (RTX 5060)
        
        # 🪄 [YOLOv11 공식 실시간 데이터 뻥튀기 파라미터 세팅]
        augment=True,      # 데이터 증강 기능 활성화
        degrees=15.0,      # 이미지를 무작위로 ±15도 회전 (카메라 각도 비틀림 대비)
        translate=0.1,     # 이미지를 상하좌우로 10%씩 평행 이동 (번호판 위치 다양화)
        scale=0.5,         # 이미지를 50%~150% 크기로 무작위 확대/축소 (원근감 대비)
        shear=5.0,         # 이미지를 무작위로 ±5도 찌그러뜨림 (사선 각도 대비)
        perspective=0.001, # 미세한 3D 원근감 효과 추가
        
        # 🎨 색상/밝기 및 노이즈 관련 공식 인자 변경 구간
        hsv_h=0.015,       # 이미지 색상(Hue) 무작위 변경 범위
        hsv_s=0.7,         # 이미지 채도(Saturation) 무작위 변경 범위 (대비 효과)
        hsv_v=0.4,         # 이미지 밝기(Value) 무작위 변경 범위 (★기존 brightness 대체)
        erasing=0.4,       # 이미지의 40% 확률로 일부를 가려 노이즈 효과 추가 (★기존 blur 기능 보완)
        mosaic=1.0,        # 4장의 사진을 무작위로 한 장으로 이어붙여 학습 (최고의 치트키 옵션)
        
        # ⚙️ 무한 증식 허용 설정
        # exist_ok=True 옵션을 아예 제거하여 학습 때마다 train-5, train-6 폴더가 계속 새로 생기도록 둡니다.
    )
    
    print("✨ 학습이 완료되었습니다! 결과 폴더 내 weights/best.pt 파일을 확인하세요.")

if __name__ == "__main__":
    main()