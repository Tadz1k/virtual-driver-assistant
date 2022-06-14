import torch
import pathlib
import time
import cv2
import numpy as np
from fastbook import *
import torch        

pathlib.PosixPath = pathlib.WindowsPath
model = 'models/model14.pkl'
learn_inf = load_learner(model)
distracted_model_pkl = torch.load('models/model14.pkl')    

fastai_preds = []
fastai_time = []

torch_preds = []
torch_time = []


def average(lst):
    return sum(lst) / len(lst)

for i in range (1, 11):
    start_time = round(time.time()*1000)
    pred, pred_idx, probs = learn_inf.predict(f'benchmark_images/{i}.jpg')
    end_time = round(time.time()*1000) - start_time
    fastai_time.append(end_time)
    fastai_preds.append(pred)

for i in range(1, 11):
    start_time = round(time.time()*1000)
    result = distracted_model_pkl.predict(f'benchmark_images/{i}.jpg')
    end_time = round(time.time()*1000) - start_time
    torch_time.append(end_time)
    torch_preds.append(result[0])


print('FASTAI PREDS:')
print(fastai_preds)
print('FASTAI AVG TIME:')
print(average(fastai_time))

print('TORCH PREDS:')
print(torch_preds)
print('TORCH AVG TIME')
print(average(torch_time))