import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        indexFinger = hand["lmList"][8]
        thumb = hand["lmList"][4]
        distance = ((indexFinger[0] - thumb[0]) ** 2 + (indexFinger[1] - thumb[1]) ** 2) ** 0.5
        if distance < 30:
            print("gotcha! coordinates:", indexFinger)
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:  #esc to close the programm
        break

cap.release()
cv2.destroyAllWindows()
