# <snippet_imports>
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from lib.azure_config import endpoint, subscription_key

from array import array
import os
from PIL import Image
import sys
import time
import sys

def detect_image(local_image_path):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    # Open local image file
    local_image = open(local_image_path, "rb")
    try:
        ocr_result_local = computervision_client.recognize_printed_text_in_stream(local_image)
        detected_s = ""
        for region in ocr_result_local.regions:
            for line in region.lines:
                print("Bounding box: {}".format(line.bounding_box))
                for word in line.words:
                    detected_s += word.text + " "
        return detected_s
    except:
        return ""