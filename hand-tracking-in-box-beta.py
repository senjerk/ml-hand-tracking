import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            if w > 200 and h > 200: #эти значения нужно самостоятельно подвигать, ибо иначе плохо работает.
                hands, img = detector.findHands(img)
                if hands:
                    hand = hands[0]
                    indexFinger = hand["lmList"][8] 
                    thumb = hand["lmList"][4] 
                    distance = ((indexFinger[0] - thumb[0]) ** 2 + (indexFinger[1] - thumb[1]) ** 2) ** 0.5
                    if distance < 30:
                        print("Касание! Координаты указательного пальца:", indexFinger)
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27: # esc to close the programm
        break

cap.release()
cv2.destroyAllWindows()
