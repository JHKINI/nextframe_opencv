# 번호판 인식 시스템 — OCR 통합 작업 정리

> 작성: 송현우 (Next Frame 팀 프로젝트)
> 대상 파일: `ocr.py`, `detection.py`, `main.py`

기존 코드는 **OCR이 "빈 껍데기"** 상태(`"인식 모델 대기 중"` 문자열만 반환)였고, `detection.py`는 흑백 이진화본 1장만 넘겨주는 구조였습니다.
이번 작업에서 **EasyOCR 실제 인식 + 형식 검증 + 다중 프레임 투표**를 붙이고, 그에 맞춰 `detection.py`와 `main.py`의 데이터 흐름을 수정했습니다.

핵심 설계 결정은 한 줄로 요약됩니다:

> **화면 표시·저장은 흑백 이진화본, OCR 입력은 컬러 원본** (이진화하면 글자가 깨져 인식률이 떨어지므로)

---

## 1. `ocr.py` — 빈 껍데기 → 실제 OCR 엔진 (신규 작성)

가장 큰 변화. 기존에는 고정 문자열만 리턴했지만, EasyOCR 기반 실제 인식 함수로 전면 교체했습니다.

### 1-1. 엔진 초기화 및 번호판 형식 정의

```python
reader = easyocr.Reader(['ko', 'en'], gpu=True)

# 번호판 형식: 숫자2~3 + 한글1 + 숫자4  (예: 12가3456, 123가4567)
PLATE_PATTERN = re.compile(r'^\d{2,3}[가-힣]\d{4}$')
```

- 한국어/영어 모델을 `gpu=True`로 로드 (속도 확보)
- 정규식으로 한국 번호판 표준 형식을 정의 → **형식에 안 맞는 인식 결과는 버림**

### 1-2. 오인식 보정: `correct_plate_text()`

```python
def correct_plate_text(text):
    text = text.replace(' ', '').strip()
    # 8자리인데 맨 앞이 '1'이면 → 앞의 1을 떼고 다시 검증
    if len(text) == 8 and text.startswith('1'):
        candidate = text[1:]
        if is_valid_plate(candidate):
            return candidate
    return text
```

- 공백 제거
- **자주 발생하는 오인식 패턴 보정**: 번호판 앞쪽 노이즈/테두리를 `1`로 잘못 읽어 8자리가 되는 경우, 앞 `1`을 떼고 7자리로 재검증

### 1-3. 형식 검증: `is_valid_plate()`

```python
def is_valid_plate(text):
    return bool(PLATE_PATTERN.match(text))
```

### 1-4. 메인 인식 함수: `read_plate()`

```python
def read_plate(cropped_plate):
    if cropped_plate is None:
        return ""                       # 빈 문자열 = "유효 결과 없음"의 약속

    # 흑백(2차원)이면 RGB로 변환해서 입력
    if len(cropped_plate.shape) == 2:
        img = cv2.cvtColor(cropped_plate, cv2.COLOR_GRAY2RGB)
    else:
        img = cropped_plate

    results = reader.readtext(
        img,
        detail=0,                       # 텍스트만 반환 (좌표 X)
        paragraph=False,
        allowlist='0123456789가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주하허호배'
    )

    if len(results) == 0:
        return ""

    text = ''.join(results)
    text = re.sub(r'[^0-9가-힣]', '', text)   # 숫자·한글만 남김
    text = correct_plate_text(text)

    if not is_valid_plate(text):        # ✅ 형식 안 맞으면 버림
        return ""
    return text
```

이 함수의 핵심 포인트:

| 항목 | 설명 |
|------|------|
| `allowlist` | 번호판에 실제 쓰이는 글자(숫자 + 한글)로만 제한 → 엉뚱한 글자 오인식 차단 |
| `detail=0` | 좌표 없이 텍스트만 받아 후처리 단순화 |
| 빈 문자열 반환 규칙 | None / 인식 실패 / 형식 불일치는 모두 `""` 반환 → 호출부에서 "버릴 결과"로 통일 처리 |

---

## 2. `detection.py` — 반환값 2개 → 3개 (OCR용 컬러 크롭 추가)

OCR이 컬러 원본을 필요로 하면서, detection이 **흑백본과 컬러본을 둘 다** 넘기도록 수정했습니다.

### 2-1. 추론 해상도 지정 + 디버그 출력

```python
print(f"DEBUG: 모델 경로 확인 -> {os.path.abspath(model_path)}")   # 모델 경로 확인용
...
results = self.model(frame, imgsz=1088, verbose=False, iou=0.7, conf=conf_thres)[0]
```

- `imgsz=1088` 추가 → 입력 해상도를 키워 **작은/먼 번호판 탐지율 향상**
- 모델 절대경로를 출력해 `best.pt` 로드 위치 디버깅

### 2-2. 탐지 로그 추가

```python
box_count = len(results.boxes)
if box_count > 0:
    print(f"객체 탐지 성공! (탐지된 객체 수: {box_count})")
    for box in results.boxes:
        ...
        print(f"Detected Class ID: {cls_id}, Confidence: {conf:.2f}")
```

### 2-3. OCR 전용 컬러 크롭 추가 (가장 중요한 변경)

```python
cropped_plate_bin = None      # 화면 표시·저장용 (흑백 이진화)
cropped_plate_color = None    # ✅ [추가] OCR 전용 (이진화 안 한 컬러 원본)
...
if vehicle_plate.size > 0:
    cropped_plate_color = vehicle_plate.copy()                    # ✅ 컬러 원본 보존

    gray_plate = cv2.cvtColor(vehicle_plate, cv2.COLOR_BGR2GRAY)
    _, cropped_plate_bin = cv2.threshold(gray_plate, 0, 255,
                                         cv2.THRESH_BINARY + cv2.THRESH_OTSU)
...
return contour_img, cropped_plate_bin, cropped_plate_color        # ✅ 2개 → 3개
```

**변경 이유:** OTSU 이진화는 화면 표시엔 깔끔하지만 글자 획이 뭉개져 OCR 정확도가 떨어집니다. 그래서 표시용(흑백)과 인식용(컬러)을 **분리**했습니다.

> ⚠️ **연동 주의:** 반환값이 2개 → 3개로 바뀌었으므로, `detect_frame()`을 호출하는 쪽은 반드시 변수 3개로 받아야 합니다. (main.py에 반영 완료)

---

## 3. `main.py` — OCR 연동 + 한글 출력 + 다중 프레임 투표

### 3-1. 신규 import 및 OCR 활성화

```python
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from collections import Counter
...
import ocr        # 기존엔 주석 처리되어 있던 것을 활성화
```

### 3-2. 한글 화면 출력 헬퍼 `put_text_kr()`

OpenCV의 `putText`는 한글이 깨지므로(□□□), **PIL로 그린 뒤 다시 OpenCV 이미지로 변환**하는 헬퍼를 추가했습니다.

```python
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
```

- 화면의 OCR 인식 결과(한글 포함)는 `put_text_kr`로 출력
- FPS 같은 영문/숫자는 기존 `cv2.putText` 그대로 사용 (속도상 이점)

### 3-3. 상태 변수 변경

```python
self.is_tracking = False
self.cycle_images = []                       # ✅ (흑백패딩본, 컬러패딩본) '쌍'으로 저장
self.last_license_number = "인식 대기 중"     # ✅ 최근 확정된 번호 유지
```

기존엔 흑백 이미지 1장만 모았지만, 이제 **(흑백, 컬러) 튜플**로 모아 OCR에 컬러를 쓸 수 있게 했습니다.

### 3-4. FPS 0 나눗셈 방어 + 단계별 처리시간 측정

```python
delta = curr_time - self.prev_time
fps = 0 if delta <= 0 else 1 / delta          # ✅ ZeroDivision 방어

t0 = time.time()   # 전처리 시작
...
t4 = time.time()   # UI 출력 끝
print(f"[TIME] 전처리:{(t1-t0)*1000:5.0f}ms | YOLO:{(t2-t1)*1000:5.0f}ms | "
      f"텍스트:{(t3-t2)*1000:5.0f}ms | UI:{(t4-t3)*1000:5.0f}ms | "
      f"합계:{total*1000:5.0f}ms ({1/total if total>0 else 0:.1f} FPS)")
```

- 각 단계(전처리 / YOLO / 텍스트 / UI) 소요 시간을 ms 단위로 출력 → **병목 구간 분석용**

### 3-5. 탐지 시 (흑백, 컬러) 쌍 수집

```python
display_frame, cropped_plate, cropped_plate_color = detector.detect_frame(frame, conf_thres=0.25)
...
# 흑백/컬러 둘 다 동일하게 흰색 패딩(15px)
padded_plate = cv2.copyMakeBorder(cropped_plate, 15,15,15,15, cv2.BORDER_CONSTANT, value=[255,255,255])
padded_color = cv2.copyMakeBorder(cropped_plate_color, ...) if cropped_plate_color is not None else None

self.display_image(padded_plate, self.screen_crop)   # 화면엔 흑백 표시

if 1.5 <= aspect_ratio <= 5.5:                        # 정상 비율만 채택
    self.cycle_images.append((padded_plate, padded_color))   # ✅ 쌍으로 저장
```

### 3-6. 추적 종료 시 — 다중 프레임 투표 OCR (정확도 핵심)

차량이 화면을 벗어나면, 한 프레임이 아니라 **여러 프레임의 OCR 결과를 모아 최빈값으로 확정**합니다.

```python
# 1) 면적 큰 순으로 상위 5장 후보 선정 (흑백본 면적 기준)
candidates = sorted(self.cycle_images,
                    key=lambda p: p[0].shape[0] * p[0].shape[1],
                    reverse=True)[:5]

# 2) 저장은 가장 큰 흑백본 1장
best_bin = candidates[0][0]
cv2.imwrite(file_path, best_bin)

# 3) 후보 5장 각각 OCR → 형식 통과한 결과만 수집
valid_results = []
for _bin, _color in candidates:
    ocr_input = _color if _color is not None else _bin   # ✅ 컬러 우선
    r = ocr.read_plate(ocr_input)
    if r:                                                 # 빈 문자열은 제외
        valid_results.append(r)

# 4) 최빈값(가장 많이 나온 결과) 채택 = 투표
if valid_results:
    best_result = Counter(valid_results).most_common(1)[0][0]
    self.last_license_number = best_result
    print(f"🔤 [OCR 투표 결과] {best_result} (후보: {valid_results})")
else:
    print("🚫 [형식 불일치] 유효한 번호판을 찾지 못했습니다.")
```

**왜 투표 방식인가?**
단일 프레임 OCR은 흔들림·각도·빛 반사에 따라 결과가 들쭉날쭉합니다. 여러 프레임 결과 중 **가장 자주 나온 값**을 고르면 일시적 오인식의 영향을 크게 줄일 수 있습니다.


## 4. 전체 데이터 흐름 (변경 후)

```
[프레임]
   │
   ▼
detection.detect_frame()
   ├─ contour_img         (박스 그려진 표시용 영상)
   ├─ cropped_plate_bin   (흑백 이진화 → 화면 표시·저장)
   └─ cropped_plate_color (컬러 원본 → OCR 입력)   ★신규
   │
   ▼  추적 중: (흑백, 컬러) 쌍을 cycle_images에 누적
   │
   ▼  추적 종료 시
   ├─ 면적 상위 5장 후보 선정
   ├─ 각 후보 → ocr.read_plate(컬러 우선)
   │        └─ EasyOCR → allowlist 필터 → 형식검증(정규식) → 보정
   └─ Counter 최빈값 투표 → 최종 번호 확정
   │
   ▼
put_text_kr() 로 화면에 한글 번호 출력
```

---

## 5. 변경 요약 (한눈에)

| 파일 | 주요 변경 | 목적 |
|------|-----------|------|
| `ocr.py` | EasyOCR 실제 구현, 정규식 형식검증, 오인식 보정, allowlist | 빈 껍데기 → 실제 인식 |
| `detection.py` | `cropped_plate_color` 추가, 반환 3개화, `imgsz=1088` | OCR용 컬러 원본 공급, 탐지율↑ |
| `main.py` | `import ocr` 활성화, `put_text_kr`, (흑백,컬러) 쌍 수집, 5장 투표 OCR, 단계별 시간측정 | 인식 연동·한글 출력·정확도·성능 분석 |

---

## 6. 남은 보완 포인트 (참고)

- `gpu=True`로 EasyOCR을 쓰므로, GPU 없는 PC에서 실행 시 `gpu=False` 분기 또는 예외 처리 권장
- `put_text_kr`는 매 프레임 PIL 변환이 일어나 비용이 있음 → OCR 결과가 바뀔 때만 갱신하는 캐싱 고려 가능
- 투표 시 동률(tie)일 경우 처리 규칙(예: 가장 큰 면적 프레임 우선)을 명시하면 더 견고함
