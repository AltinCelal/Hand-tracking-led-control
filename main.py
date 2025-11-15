import cv2
import mediapipe as mp
import serial
import time

# ---- Seri port ----
ser = serial.Serial("COM5", 115200)

# ---- Mediapipe ----
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

# ---- Kamera ----
cap = cv2.VideoCapture(0)

# ---- Kutu ayarları ----
boxes = {
    "B": ((50, 50), (200, 200), (255, 0, 0)),       # Mavi
    "Y": ((250, 50), (400, 200), (0, 255, 255)),      # Yeşil
    "R": ((450, 50), (600, 200), (0, 0, 255))       # Kırmızı
}

# ---- 3 Hz veri gönderme ----
last_send = 0
SEND_PERIOD = 1   # saniyede 3 kez

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    # RGB
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    finger_x, finger_y = None, None

    # ---- İşaret parmağı ----
    if results.multi_hand_landmarks:
        for hand_lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)

            x = int(hand_lm.landmark[8].x * w)
            y = int(hand_lm.landmark[8].y * h)
            finger_x, finger_y = x, y

    # ---- Kutu işlemleri ----
    for key, (pt1, pt2, color) in boxes.items():
        cv2.rectangle(frame, pt1, pt2, color, 2)

        if finger_x is not None:
            if pt1[0] < finger_x < pt2[0] and pt1[1] < finger_y < pt2[1]:

                now = time.time()

                # Sadece 3 Hz gönder
                if now - last_send >= SEND_PERIOD:
                    ser.write(key.encode())
                    last_send = now
                    print("Gönderildi:", key)

                cv2.putText(frame, f"{key}",
                            (pt1[0], pt1[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
