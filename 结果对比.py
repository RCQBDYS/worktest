import pytesseract
from PIL import Image

if __name__ == '__main__':
    text = pytesseract.image_to_string(Image.open("E:\\test3.png"), lang="eng")
    print(text)