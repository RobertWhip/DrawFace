import cv2
import numpy as np


class FaceDetector:
    def __init__(self, test_mode=False):
        self.__test_mode = test_mode

    def nothing(self):
        pass

    def get_face_contour_lines(self):
        cap = cv2.VideoCapture(0)
        neighbours = 4

        _, frame = cap.read()
        face_cascade = cv2.CascadeClassifier("haar.xml")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, neighbours)

        x, y, w, h = faces[0]
        edges = cv2.Canny(gray[y:y + h, x:x + w], 100, 150)
        _, thresh = cv2.threshold(edges, 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if self.__test_mode:
            result = np.zeros((480, 640, 3), np.uint8)
            b = 50
            g = 50
            r = 50
            for contour in contours:
                epsilon = 0.001 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                cv2.drawContours(result, [approx], -1, (b % 256, g % 256, r % 256), 3)
                b += 1
                g += 2
                r += 3
            while True:
                cv2.imshow("Result", result)
                k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    break
        cap.release()
        return self.get_contour_lines(contours)

    @staticmethod
    def get_contour_lines(contours):
        lines = []
        # e = 0.001
        for contour in contours:
            line = []
            # epsilon = e * cv2.arcLength(contour, True)
            # approx = cv2.approxPolyDP(contour, epsilon, True)
            # cv2.drawContours(frame, [approx], -1, (b % 256, g % 256, r % 256), 3)
            for point in contour:  # for contour in approx:
                line.append((point[0][0], point[0][1]))
            if len(line) > 1:
                lines.append(line)
        return lines


if __name__ == "__main__":
    fd = FaceDetector(test_mode=True)
    print(fd.get_face_contour_lines())
