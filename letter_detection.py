import cv2
import numpy as np
import pytesseract
import string
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'


def find_letters_cords(image_filename):
    img = cv2.imread(image_filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = items[0] if len(items) == 2 else items[1]

    img_contour = img.copy()
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if 100 < area < 10_000:
            cv2.drawContours(img_contour, contours, i, (0, 0, 255), 2)

    letters_cords = {}
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        ratio = h/w
        area = cv2.contourArea(contour)
        base = np.ones(thresh.shape, dtype=np.uint8)
        if ratio > 0.9 and 100 < area < 10_000:
            base[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]
            segment = cv2.bitwise_not(base)

            custom_config = r'-l eng --psm 10'
            ocr_result = pytesseract.image_to_string(segment, config=custom_config)

            if len(ocr_result) == 0:
                continue
        
            ocr_char = ocr_result[0].upper()

            # because of their font, OCR detects 'I' as '|' (vertical line)
            if ocr_char == '|':
                ocr_char = 'I'
            if ocr_char == '-':
                ocr_char = 'F'

            print(f"detected letter: {ocr_char}")

            if ocr_char in string.ascii_letters:
                relative_cord = (x, y)
                letters_cords[relative_cord] = ocr_char
            
            cv2.imshow("segment", segment)
            cv2.waitKey(0)

    return letters_cords


def cut_letter_wheel(img: Image):
    width, height = img.size
    # my screen size: 1080x2340
    left = 190
    right = width-left
    upper = height/2 + 200
    lower = height-280

    return ((left, upper), img.crop((left, upper, right, lower)))


def transform_cords(dimensions, letters_cords: dict[tuple, str]):
    # perform domain expansion (ryoiki tenkai)

    left, upper = dimensions

    transformed_cords = {}
    for cord in letters_cords.keys():
        x, y = cord
        x += left
        y += upper
        transformed_cords[(x,y)] = letters_cords[cord]

    return transformed_cords


def find_transformed_letters_cords(filename):
    img = Image.open(filename)

    new_dimensions, letter_wheel_img = cut_letter_wheel(img)
    letter_wheel_img.save("wheel.png")

    letters_cords = find_letters_cords("wheel.png")

    letters_cords = transform_cords(new_dimensions, letters_cords)
    return letters_cords
