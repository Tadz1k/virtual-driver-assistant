import torch
import cv2
import time


def current_milli_time():                                                                   # get current time in milliseconds
    return round(time.time() * 1000)                                                        

#model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # local model
model = torch.hub.load('yolov5', 'custom', path='models\yolov5s.pt', source='local')  # local repo
model.conf = 0.45

image = cv2.imread('test.jpg')
image = cv2.resize(image, (640, 640))

start_millis = current_milli_time()
results = model(image)
#results.print()
results.print()
end_millis = current_milli_time()
print(end_millis - start_millis)


#pip3 install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html