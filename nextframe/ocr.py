import easyocr
import cv2
import re

reader = easyocr.Reader(['ko', 'en'], gpu=True)

# 번호판 형식: 숫자2~3 + 한글1 + 숫자4
PLATE_PATTERN = re.compile(r'^\d{2,3}[가-힣]\d{4}$')

def correct_plate_text(text):
    text = text.replace(' ', '').strip()

    if len(text) == 8 and text.startswith('1'):
        candidate = text[1:]
        if is_valid_plate(candidate):
            return candidate
        
    return text


def is_valid_plate(text):
    """번호판 형식에 맞으면 True"""
    return bool(PLATE_PATTERN.match(text))


def read_plate(cropped_plate):
    if cropped_plate is None:
        return ""  # 빈 문자열 = 유효 결과 없음

    if len(cropped_plate.shape) == 2:
        img = cv2.cvtColor(cropped_plate, cv2.COLOR_GRAY2RGB)
    else:
        img = cropped_plate

    results = reader.readtext(
        img,
        detail=0,
        paragraph=False,
        allowlist='0123456789가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주하허호배'
    )

    if len(results) == 0:
        return ""

    text = ''.join(results)
    text = re.sub(r'[^0-9가-힣]', '', text)
    text = correct_plate_text(text)

    # ✅ 형식 검증: 안 맞으면 빈 문자열 반환
    if not is_valid_plate(text):
        return ""

    return text
