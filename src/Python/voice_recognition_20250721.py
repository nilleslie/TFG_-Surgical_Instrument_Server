import speech_recognition as sr
import numpy as np
import cv2
import threading
import difflib
from ultralytics import YOLO
from pymodbus.client import ModbusTcpClient
from pyModbusTCP.server import ModbusServer

import time
from time import sleep

# CONFIG

H = np.load("MAT_H_LAB2.npy")
model = YOLO("best.pt")
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
mic = sr.Microphone(device_index=3)
recognizer = sr.Recognizer()
last_command = None
detected_objects = {}

server = ModbusServer("84.88.129.100", 502, no_block=True)
print("Server MODBUS active in 84.88.129.100:502")
server.start()

# Coordinate conversion
def pixel_to_world(u, v, H):
    pixel = np.array([u, v, 1], dtype='float32')
    world = H @ pixel
    world /= world[2]
    

    return world[0] , world[1] 



#Translation of words in spanish to english
translation_dict = {
    "tijeras": "scissors",
    "cuchillo": "knife",
    "pinzas": "tweezers",
    
}
def fuzzy_translate(command, translation_dict, threshold=0.6):
    if not command:
        return None

    possibles = list(translation_dict.keys())
    millor_candidata = difflib.get_close_matches(command.lower(), possibles, n=1, cutoff=threshold)
    if millor_candidata:
        return translation_dict[millor_candidata[0]]
    return None


# Send coords + activate bit
# offset of the coordinates due to the tcp
tox = 1.0  # cm (left)
toy = -4.0   # cm (back)
toz = 0   # cm (down)


def send_coords_to_modbus(x_cm, y_cm, z_cm=-0.8 ):
    try:       
        x_i = int(abs(x_cm+tox) * 10)
        y_i = int(abs(y_cm+toy) * 10)
        z_i = int(abs(z_cm+toz) * 10)

        #Calculating the sign (1 if it's negartive, 0 if it's positive)
        s_x = int(x_cm <0)
        s_y = int(y_cm <0)
        s_z= int(z_cm <0)

        #Writting the coordinates
        server.data_bank.set_input_registers(24, [x_i])
        server.data_bank.set_input_registers(34, [y_i])
        server.data_bank.set_input_registers(44, [z_i])

        # Writting the signs
        server.data_bank.set_input_registers(55, [s_x])
        server.data_bank.set_input_registers(65, [s_y])
        server.data_bank.set_input_registers(75, [s_z])

    
        
        server.data_bank.set_input_registers(85, [1])  # Activation bit ON
        print(f"Sent: X={x_i} Y={y_i} Z={z_i} mm | Signs: {s_x}, {s_y}, {s_z} | Bit 10 = True")
        sleep(0.5)
        server.data_bank.set_input_registers(85, [0]) # Reset activation bit
        sleep(1)
    except Exception as e:
        print(f"Server error: {e}")
        server.stop()

# Voice thread
def continuous_listening():
    global last_command
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Voice listening activated.")
        while True:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                text = recognizer.recognize_google(audio, language="es-ES")
                print(f"Command: {text}")
                last_command = text.lower()
            except: continue

threading.Thread(target=continuous_listening, daemon=True).start()

# MAIN LOOP
while True:
    

    ret, frame = cap.read()
    if not ret:
        break
    sent_this_cycle = False 
    results = model(frame, conf=0.82) #0.82 the best result 
    annotated = frame.copy()
    detected_objects.clear()

    for box in results[0].boxes:
        cls_id = int(box.cls[0].item())
        label = model.names[cls_id].lower()
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        u, v = int((x1 + x2) / 2), int((y1 + y2) / 2)
        X, Y = pixel_to_world(u, v, H)
        detected_objects[label] = (u, v, X, Y)

    #translating voice command to english 
    if last_command:
        translated = fuzzy_translate(last_command, translation_dict)
    else:
        translated = None
    #Search for a match between the command and the objects 

    matched_object = translated if translated in detected_objects else ""

    if matched_object and not sent_this_cycle:
        _, _, X_match, Y_match = detected_objects[matched_object]
        print(f"Matched: {matched_object.upper()} at {X_match:.1f}, {Y_match:.1f} cm")
        send_coords_to_modbus(X_match, Y_match)
        sent_this_cycle = True
    for label, (u, v, X, Y) in detected_objects.items():
        color = (0, 0, 255) if label == matched_object else (0, 255, 0)
        cv2.circle(annotated, (u, v), 5, color, -1)
        cv2.putText(annotated, f"{label}: ({X:.1f}, {Y:.1f})", (u, v - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    if not matched_object:
        sent_this_cycle = False

    cv2.imshow("Detection + Voice", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
