import argparse

import cv2
import pytesseract
import re
import pandas as pd
import numpy as np
from lib.swt import do_swt
from lib.azure_vision import detect_image
pytesseract.pytesseract.tesseract_cmd = r"tesseract"
config = ('-l eng --oem 3 --psm 11')

BIL_FILTER = [1, 5, 5]
THRESHOLD = [50, 255]

def bib_detector(im):
    height, width, channels = im.shape
    if width>50:
        cv2.imwrite('./temp.jpg', im)
        return detect_image('./temp.jpg') 
    else:
        return "Too small torso detected"
        
def text_detection_filter(im):
    im = cv2.bilateralFilter(im, BIL_FILTER[0], BIL_FILTER[1], BIL_FILTER[2])
    # Straigten edges (not pixely)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.Canny(im,150,200)
    #im = cv2.dilate(im, np.ones((2, 2)))
    ret, im = cv2.threshold(im, THRESHOLD[0], THRESHOLD[1], cv2.THRESH_BINARY)

    im = cv2.blur(im, (2, 1))
    cv2.imshow("Preprocessed for number detector ",im)
    cv2.waitKey(0)
    # Run tesseract OCR on image
    text = pytesseract.image_to_string(im, config=config)
    print("Found text ", text)

    return extract_numbers(text)

def extract_numbers(text):
    km_regex = re.compile('[0-9]+')

    if km_regex.search(text):
        try:
            km_string = str(km_regex.search(text).group(1))
            km_string = km_string.replace(",", ".")
            return float(km_string)
        except ValueError:
            return -1.0
    else:
        return -1.0