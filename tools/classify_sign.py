import torch       
import cv2        
import pathlib
import numpy as np
pathlib.PosixPath = pathlib.WindowsPath
speed_limit_model_pkl = torch.load('../models/speed-limits.pkl')

image = cv2.imread('ograniczenie.jpg')
image = cv2.resize(image, (50, 50))
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = np.asarray(image)

result = speed_limit_model_pkl.predict(image)[0]
cv2.putText(image, result[0])
cv2.imshow(image)

print(result)