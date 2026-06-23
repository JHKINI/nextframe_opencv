import easyocr
import cv2
import re
import os
import time

reader = easyocr.Reader(['ko', 'en'], gpu=True)

# 사업용 번호판 앞에 붙는 지역명 (2글자, 17개 시·도)
REGIONS = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
    '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주',
]
REGION_PATTERN = '|'.join(REGIONS)

# 일반 번호판:  숫자2~3 + 한글1 + 숫자4        (예: 12가3456, 123가4567)
PLATE_PATTERN = re.compile(r'^\d{2,3}[가-힣]\d{4}$')

# 사업용 번호판: 지역명 + 숫자2 + 한글1 + 숫자4   (예: 서울12바3456)
PLATE_PATTERN_REGION = re.compile(rf'^(?:{REGION_PATTERN})\d{{2}}[가-힣]\d{{4}}$')

# ── OCR allowlist 구성 ──────────────────────────────────────────
# 번호판 용도 기호로 쓰이는 한글
BASE_HANGUL = '가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주하허호배'
# 지역명에 등장하는 한글(중복 자동 제거) → 이게 없으면 지역명이 OCR에서 아예 안 나옴
REGION_HANGUL = ''.join(set(''.join(REGIONS)))
ALLOWLIST = ''.join(sorted(set('0123456789' + BASE_HANGUL + REGION_HANGUL)))


def is_valid_plate(text):
    """일반 또는 사업용 형식 중 하나라도 맞으면 True"""
    return bool(PLATE_PATTERN.match(text) or PLATE_PATTERN_REGION.match(text))


def read_plate(cropped_plate):
    if cropped_plate is None:
        return ""  # 빈 문자열 = 유효 결과 없음

    if len(cropped_plate.shape) == 2:
        img = cv2.cvtColor(cropped_plate, cv2.COLOR_GRAY2RGB)
    else:
        img = cropped_plate

    img = cv2.resize(
        img,
        None,
        fx=2.5,
        fy=2.5,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    debug_dir = "ocr_debug"
    os.makedirs(debug_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    debug_path = os.path.join(debug_dir, f"ocr_input_{timestamp}.png")

    # img는 RGB라서 OpenCV 저장용 BGR로 변환
    cv2.imwrite(debug_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    print(f"🖼️ [OCR 입력 이미지 저장] {debug_path}")

    results = reader.readtext(
        img,
        detail=1,
        paragraph=False,
        allowlist=ALLOWLIST,
    )

    if len(results) == 0:
        return ""

    # 왼쪽 x좌표 기준 정렬
    results = sorted(results, key=lambda r: min(p[0] for p in r[0]))

    texts = [r[1] for r in results]
    text = ''.join(texts)

    print("[OCR RAW]", texts, "=>", text)

    # ✅ 형식 검증: 일반/사업용 둘 다 통과 못 하면 빈 문자열
    if not is_valid_plate(text):
        return ""

    return text