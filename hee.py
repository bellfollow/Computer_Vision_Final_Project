import cv2
import mediapipe as mp
import pyautogui
import time

def press_key(key):
    if key == 'A':
        pyautogui.hotkey('win', 'tab')
    elif key == 'B':
        pyautogui.hotkey('win')
    elif key == 'C':
        pyautogui.hotkey('alt','tab')
    elif key == 'D':
        pyautogui.press('esc')
    elif key == 'E':
        pyautogui.press('enter')
    elif key == 'F':
        pyautogui.hotkey('ctrl', 'w')
    elif key == 'G':
        pyautogui.hotkey('ctrl', 't')
    elif key == 'H':
        pyautogui.hotkey('ctrl', 'a')
    elif key == 'I':
        pyautogui.hotkey('ctrl', 'x')


def compare_f(a1, a2):
    a = hand_landmarks.landmark[a1].y
    b = hand_landmarks.landmark[a2].y
    return a < b


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

x1, y1, x2, y2 = 100, 100, 600, 400

start_time = time.time()
check_interval = 2

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)  # 영상 좌우 반전

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)


    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if x1 < cx < x2 and y1 < cy < y2:
                    cv2.putText(img, "keyboard mode on", (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2,cv2.LINE_AA)
                    cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    if time.time() - start_time >= check_interval:
                        # 손가락 관절 위치 비교 및 제스처 판별
                        if compare_f(4, 17) and not compare_f(8, 6) and not compare_f(12, 10) and not compare_f(16, 14) and not compare_f(20, 18):
                            press_key('A')
                        elif compare_f(4, 17) and compare_f(8, 6) and not compare_f(12, 10) and not compare_f(16, 14) and not compare_f(20, 18):
                            press_key('B')
                        elif compare_f(4, 17) and compare_f(8, 6) and compare_f(12, 10) and not compare_f(16, 14) and not compare_f(20, 18):
                            press_key('C')
                        elif compare_f(4, 17) and compare_f(8, 6) and compare_f(12, 10) and compare_f(16, 14) and not compare_f(20, 18):
                            press_key('D')
                        elif compare_f(4, 17) and compare_f(8, 6) and compare_f(12, 10) and compare_f(16, 14) and compare_f(20, 18):
                            press_key('E')
                        elif compare_f(20, 18) and not compare_f(16, 14) and not compare_f(12, 10) and not compare_f(8, 6) and not compare_f(4, 17):
                            press_key('F')
                        elif compare_f(20, 18) and compare_f(16, 14) and not compare_f(12, 10) and not compare_f(8, 6) and not compare_f(4, 17):
                            press_key('G')
                        elif compare_f(20, 18) and compare_f(16, 14) and not compare_f(12, 10) and not compare_f(8, 6) and not compare_f(4, 17):
                            press_key('H')
                        elif compare_f(20, 18) and compare_f(16, 14) and compare_f(12, 10) and not compare_f(8, 6) and not compare_f(4, 17):
                            press_key('I')

                        start_time = time.time()  # 시간 초기화

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Gotcha", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    if time.time() - start_time >= check_interval:
        start_time = time.time()  # 시간 초기화
cap.release()
cv2.destroyAllWindows()
