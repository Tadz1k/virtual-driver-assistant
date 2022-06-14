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

model_pkl = torch.load('../models/distracted_model.pkl')
video = cv2.VideoCapture('../data/distracted.mp4')
capture, image = video.read()


while video.isOpened():
    ret, frame = video.read()
    if ret is True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (640, 480))
        result = model_pkl.predict(resized)
        print(states[result[0]])
        cv2.imshow('Frame', gray)
        if cv2.waitKey(1) and 0xFF == ord ('q'):
            break
    else:
        break
video.release()
cv2.destroyAllWindows()

