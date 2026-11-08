# NextFrame ALPR – 차량 번호판 탐지

## 프로젝트 소개
YOLO26n 기반 객체 탐지 모델을 학습해 차량 이미지와 영상에서 번호판 영역을 탐지하는 프로젝트입니다.

## 주요 작업
- Roboflow YOLO 형식의 번호판 데이터셋을 이용한 학습 환경 구성
- Ultralytics YOLO26n 사전 학습 모델 파인튜닝
- 테스트 이미지 대상 번호판 탐지
- 차량 영상 대상 프레임별 번호판 탐지 및 결과 저장

## 기술 스택
- Python
- Ultralytics YOLO26n
- PyTorch
- OpenCV (영상 처리 기반)
- Google Colab / GPU

## 학습 설정
| 항목 | 설정 |
|---|---|
| 모델 | YOLO26n |
| 클래스 | `LP` (License Plate) |
| Epochs | 50 |
| Image size | 640 |
| Batch size | 8 |
| Patience | 20 |

## 검증 결과
학습 로그에서 `best.pt`를 대상으로 출력된 검증 지표입니다.

| 지표 | 결과 |
|---|---:|
| Precision | 0.997 |
| Recall | 0.993 |
| mAP@0.5 | 0.995 |
| mAP@0.5:0.95 | 0.871 |

> 위 수치는 학습에 사용된 validation 데이터 기준입니다. 독립적인 test set 평가 결과와 혼동하지 않도록 구분했습니다.

## 실행 방법
1. `NextFrame_ALPR_YOLO26_clean.ipynb`를 Google Colab에서 엽니다.
2. 런타임 유형을 GPU로 설정합니다.
3. 노트북의 데이터셋 업로드 단계에서 Roboflow YOLO 형식 ZIP 파일을 업로드합니다.
4. 셀을 위에서부터 순서대로 실행합니다.
5. 영상 추론 단계에서 테스트 영상을 업로드합니다.

## 결과 파일
- `runs/detect/license_plate_yolo26/weights/best.pt`: 학습된 모델 가중치
- `runs/detect/license_plate_yolo26/results.png`: 학습 결과 그래프
- `runs/detect/license_plate_yolo26/results.csv`: epoch별 학습 지표
- `runs/detect/predict*/`: 이미지·영상 추론 결과
## 파일구성
```text
NextFrame_ALPR/
├── README.md
├── NextFrame_ALPR_YOLO26_clean.ipynb
└── results/
    ├── training_result.png
    └── license_plate_result.zip
```

데이터셋 원본, 대용량 가중치(`best.pt`), 원본 영상은 용량 및 배포 권한을 확인한 뒤 별도 관리합니다.

## 참고
본 프로젝트는 번호판 **영역 탐지(Object Detection)** 를 수행합니다. 번호판 문자를 읽는 OCR 기능은 별도 단계이며, 이 노트북의 구현 범위에는 포함되지 않습니다.
