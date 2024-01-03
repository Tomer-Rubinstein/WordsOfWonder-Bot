import pytesseract
from PIL import Image, ImageFilter, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'

img = Image.open('screen.png')
width, height = img.size

left = 200
upper = height/2 + 200
right = width-left
lower = height - 280
 
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(10)
img = img.crop((left, upper, right, lower))
img.save("yo.png")
print(pytesseract.image_to_string(img, lang='eng', config='--psm 7'))
# print(pytesseract.image_to_boxes(img))

"""
left = 250
upper = height/2 + 200
right = width-left
lower = upper+200
for i in range(3):
    img1 = img.crop((left, upper, right, lower))
    # img1 = img1.convert("L")
    img1 = img1.filter(ImageFilter.BoxBlur(5))
    img1.save(f"yo{i+1}.png")

    print(pytesseract.image_to_string(Image.open(f'yo{i+1}.png'), lang='eng', config='--psm 6'))

    upper += 200
    lower += 200
"""
