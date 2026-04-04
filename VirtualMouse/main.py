import cv2
import mediapipe as mp
import pyautogui
import math
import time
import numpy as np
import threading
import speech_recognition as sr

# --- SETTINGS ---
SMOOTHING = 5
HAND_CLICK_DIST = 40
EYE_BLINK_DIST = 0.010
MOUSE_SENSITIVITY = 1.3

# --- SETUP ---
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.6, min_tracking_confidence=0.6)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6)

plocX, plocY = 0, 0
last_click_time = 0
voice_command = "Listening..." # Screen pe dikhane ke liye

# --- VOICE CONTROL FUNCTION (Background Thread) ---
def listen_voice():
    global voice_command
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    while True:
        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # print("Listening...") # Debugging
                audio = recognizer.listen(source, phrase_time_limit=3) # 3 sec max sunega
                
                command = recognizer.recognize_google(audio).lower()
                voice_command = f"Cmd: {command}"
                print(f"User said: {command}")

                # --- COMMANDS MAPPING ---
                if 'click' in command or 'ok' in command:
                    pyautogui.click()
                elif 'right click' in command:
                    pyautogui.rightClick()
                elif 'cut' in command:
                    pyautogui.hotkey('ctrl', 'x')
                elif 'copy' in command:
                    pyautogui.hotkey('ctrl', 'c')
                elif 'paste' in command:
                    pyautogui.hotkey('ctrl', 'v')
                elif 'scroll up' in command:
                    pyautogui.scroll(300)
                elif 'scroll down' in command:
                    pyautogui.scroll(-300)
                elif 'exit' in command or 'stop' in command:
                    break
                    
        except sr.UnknownValueError:
            pass # Agar samajh nahi aaya to ignore karo
        except Exception as e:
            print(f"Voice Error: {e}")

# Thread start kar rahe hain (Taaki video hang na ho)
voice_thread = threading.Thread(target=listen_voice)
voice_thread.daemon = True # Main program band hote hi ye bhi band ho jayega
voice_thread.start()

print("System Started with VOICE CONTROL. Speak 'Click', 'Cut', 'Paste'...")

while True:
    success, frame = cap.read()
    if not success: break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 1. Process Hand
    hand_results = hands.process(rgb_frame)

    if hand_results.multi_hand_landmarks:
        for hand_lms in hand_results.multi_hand_landmarks:
            lm = hand_lms.landmark
            x1, y1 = int(lm[8].x * w), int(lm[8].y * h)
            
            # Coordinates Mapping
            x3 = np.interp(x1, (100, w-100), (0, screen_w * MOUSE_SENSITIVITY))
            y3 = np.interp(y1, (100, h-100), (0, screen_h * MOUSE_SENSITIVITY))
            
            clocX = plocX + (x3 - plocX) / SMOOTHING
            clocY = plocY + (y3 - plocY) / SMOOTHING
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY
            
            # Click Logic
            x2, y2 = int(lm[4].x * w), int(lm[4].y * h)
            dist = math.hypot(x1 - x2, y1 - y2)
            cv2.circle(frame, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            
            if dist < HAND_CLICK_DIST:
                if time.time() - last_click_time > 0.5:
                    pyautogui.click()
                    last_click_time = time.time()
                    cv2.putText(frame, "CLICK!", (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 2. Face Fallback
    else:
        face_results = face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            for face_lms in face_results.multi_face_landmarks:
                lm = face_lms.landmark
                nose_x, nose_y = int(lm[1].x * w), int(lm[1].y * h)
                
                x3 = np.interp(nose_x, (150, w-150), (0, screen_w * MOUSE_SENSITIVITY))
                y3 = np.interp(nose_y, (150, h-150), (0, screen_h * MOUSE_SENSITIVITY))
                
                clocX = plocX + (x3 - plocX) / SMOOTHING
                clocY = plocY + (y3 - plocY) / SMOOTHING
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
                
                left_eye = abs(lm[159].y - lm[145].y)
                right_eye = abs(lm[386].y - lm[374].y)
                
                if left_eye < EYE_BLINK_DIST and right_eye < EYE_BLINK_DIST:
                    if time.time() - last_click_time > 1.0:
                        pyautogui.click()
                        last_click_time = time.time()

    # Voice Command Status on Screen
    cv2.putText(frame, voice_command, (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    cv2.imshow("AI Mouse + Voice", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()