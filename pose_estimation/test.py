import cv2
import time
import numpy as np
import sys

MODE = "COCO"

class NumberDetector():
    def __init__(self):
        if MODE is "COCO":
            self.protoFile = "pose/coco/pose_deploy_linevec.prototxt"
            self.weightsFile = "pose/coco/pose_iter_440000.caffemodel"
            self.nPoints = 18
            self.POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

        elif MODE is "MPI" :
            self.protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            self.weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
            self.nPoints = 15
            self.POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

        self.torso_detector = cv2.CascadeClassifier('person/haarcascade_fullbody.xml')

    def detect_number_people(self, img_path):
        print("Detecting runners in ",img_path)
        frame = cv2.imread(img_path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        runners = self.torso_detector.detectMultiScale(gray, 1.03, 10, flags = cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in runners:
            roi_color = frame[y:y + h, x:x + w]
            print("[INFO] Object found. Saving locally.")
            cv2.imwrite('runners/'+str(w) + str(h) + '_faces.jpg', roi_color)

if __name__ == "__main__":
    nd = NumberDetector()
    nd.detect_number_people(sys.argv[1])