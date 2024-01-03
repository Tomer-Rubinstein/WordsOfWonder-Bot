import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
SCREENSHOT_FILENAME = "screen.png"


def mask_image(img: Image, cords: tuple[int, int]) -> Image:
    org_img_arr = np.array(img)
    height, width, _ = org_img_arr.shape

    # for every tap coordinate, splash letter with white circle 
    hidden_letters_img = ImageDraw.Draw(img)
    radius = 100
    white_color = (255, 255, 255, 255)
    for cord in cords:
        x, y = cord
        left_up_point = (x-radius, y-radius)
        right_down_point = (x+radius, y+radius)
    
        hidden_letters_img.ellipse(
            [left_up_point, right_down_point],
            fill=white_color
        )
    
    modified_img_arr = np.array(img)

    # paint all non-white pixels as white
    img_mask_arr = np.array(modified_img_arr)
    red_pixel = np.array([255, 0, 0, 255])
    white_pixel = np.array([255, 255, 255, 255])
    for i in range(height):
        for j in range(width):
            curr_pixel = modified_img_arr[i, j]
            if not np.array_equal(curr_pixel, white_pixel):
                img_mask_arr[i, j] = red_pixel

    # mask (img_mask_arr & img_arr)
    for i in range(height):
        for j in range(width):
            mask_pixel = img_mask_arr[i, j]
            if np.array_equal(mask_pixel, red_pixel):
                org_img_arr[i, j] = white_pixel


    return Image.fromarray(np.uint8(org_img_arr)).convert("RGBA")


def recognize_letter(cord: tuple[int, int], img) -> str:
    cord_x, cord_y = cord
    padding = 120

    # crop image
    left = cord_x-padding
    right = cord_x+padding
    upper = cord_y-padding
    lower = cord_y+padding
    img = img.crop((left, upper, right, lower))
    img = img.filter(ImageFilter.MinFilter)

    img.save("test.png")

    custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz|"'
    return pytesseract.image_to_string(img, config=custom_config)


def recognize_letters(cords_list: list[tuple], device):
    # screen = device.screencap()
    # with open(SCREENSHOT_FILENAME, "wb") as f:
    #     f.write(screen)

    img = Image.open(SCREENSHOT_FILENAME)

    # remove the fade from the letter wheel to make it totally white
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(10)

    # remove backgrond noise
    # img = mask_image(img, cords_list)
    # img.save("first_test.png")

    # DEBUG
    debug_image = Image.open("first_test.png")

    for cord in cords_list:
        ocr_result = recognize_letter(cord, debug_image)
        if len(ocr_result) == 0: continue
        ocr_char = ocr_result[0].upper()
        if ocr_char == '|':
            ocr_char = 'I' # because of their font, vertical line looks like I

        print(ocr_char)
