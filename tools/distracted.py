import torch
import pathlib
import time
import cv2
import numpy as np

pathlib.PosixPath = pathlib.WindowsPath

states = { "c0": "Bezpieczna jazda",
"c1": "Smsy w prawej dłoni",
"c2": "Rozmowa przez telefon w prawej dłoni",
"c3": "Smski w lewej dłoni",
"c4": "Rozmowa przez telefon w lewej dłoni",
"c5": "Ustawianie radia",
"c6": "Spożywanie posiłku",
"c7": "Patrzenie w tył",
"c8": "Makeup",
"c9": "Rozmowa z pasażerem" }

def current_milli_time():
    return round(time.time() * 1000)

def get_list_avg(list):
    return sum(list)/len(list)

model_pkl = torch.load('models/densenet201_distracted.pkl')
video = cv2.VideoCapture('data/distracted.mp4')
capture, image = video.read()
times = []


while video.isOpened():
    ret, frame = video.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (640, 480))
        start_time = current_milli_time()
        result = model_pkl.predict(resized)
        end_time = current_milli_time()
        times.append(end_time - start_time)
        print(states[result[0]])
        cv2.imshow('Frame', gray)
        if cv2.waitKey(1) and 0xFF == ord ('q'):
            break
    else:
        break
video.release()
cv2.destroyAllWindows()

print(times)
print(get_list_avg(times))
print(len(times))
#resnet_50 - 75.40517241379311
#densenet_201 - 119.2758

