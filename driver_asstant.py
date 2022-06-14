#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Title: Intelligent car assistant
# @Author: Adrian Kordas
# @Date: 2022.06.14



from concurrent.futures import process
from time import time
import torch                                                                                
from threading import Thread                                                                
import pathlib                                                                              
import cv2    
from fastbook import *                                                                            

# Own imports
import screen
import tools

# Comment if script is running on another enviroment than MS Windows
pathlib.PosixPath = pathlib.WindowsPath

# File pathes                                                                                            
distracted_model_path = 'models/distracted_model.pkl'                                    
speed_limit_model_path = 'models/speed-limits.pkl'
distracted_video_path = 'data/distracted.mp4'
sign_detection_video_path = 'data/video4.mp4' 
# Model loaders                                               
sign_detection_model = torch.hub.load('yolov5', 'custom', path='models/best.pt', source='local')   
distracted_model = load_learner(distracted_model_path)
speed_limit_model = load_learner(speed_limit_model_path)
sign_detection_model.conf = 0.40                                                                                                         
                                                                                            
                                                                                            
distracted_states = {'c0': 'Safe driving', 'c1': 'Texting - right', 'c2': 'Talking - right', 'c3': 'Texting - left',
'c4': 'Talking - left', 'c5': 'Radio', 'c6': 'Drinking', 'c7': 'Behind', 'c8': 'hair', 'c9': 'Passenger'}                                                                                      
active_images = {'equal' : False, 'speedlimit' : False, 'city-enter' : False, 'stop' : False,
'crosswalk' : False, 'speed-control' : False, 'city-exit' : False}                                                                                        
repeats = {'equal' : 0, 'speedlimit' : 0, 'city-enter' : 0, 'stop' : 0, 'crosswalk' : 0, 'speed-control' : 0,
'city-exit' : 0, 'trafficlight': 0}                                                                                     
last_icon_update_time = {'equal' : 0, 'speedlimit' : 0, 'city-enter' : 0, 'stop' : 0,'crosswalk' : 0,
'speed-control' : 0, 'city-exit' : 0, 'trafficlight': 0}

# Limitations, flags and global variables                                                                             
sign_minimum_repeat = 8                                                                      
icon_time_to_live = 5000                                                                    
trafficlight_pause = 20000                                                                  
city_signs_time_to_live = 60000                                                                                                                                                                                          
alarm_pause = 10000                                                                         
alarm_start_millis = 0                                                                      
alarm_time_to_live = 5000                                                                   
speed_limit_classification_pause = 5000
max_distraction_time = 2000
speed_limit_classification_confidence = (sign_minimum_repeat-2)
safe_driving_minimum_repeat = 5
                                                                                            
distracted = False                                                                           
is_city_seen = False                                                                        
alarm_running = False                                                                       
presentation = True   

last_alarm_millis = 0                

# Create interface for traffic signs representation
root = screen.set_screen("455x200+100+100")                                                  

# Function for driver-distraction thread
def distracted_task():                                                                       
    global distracted                                                                        
    video = cv2.VideoCapture(distracted_video_path)                                          
    capture, image = video.read()                                                            
    last_distraction_time = 0
    temp_distracted = False # Distraction flag at the moment
    safe_driving_times = 0
    while video.isOpened():                                                                  
        ret, frame = video.read()
        if ret is True:
            resized = cv2.resize(frame, (640, 480))                                          
            result = distracted_model.predict(resized)                                   
            driver_status = distracted_states.get(result[0])
            if driver_status != 'Safe driving' and driver_status != 'Behind':   # 'Safe statuses'                        
                if not temp_distracted:
                    last_distraction_time = tools.current_milli_time()
                    temp_distracted = True
                # If driver is distracted for some time
                if temp_distracted and (tools.current_milli_time() - last_distraction_time) >= max_distraction_time:
                    distracted = True
            else:
                safe_driving_times += 1
                if(safe_driving_times >= safe_driving_minimum_repeat):
                    temp_distracted = False
                    distracted = False
                    safe_driving_times = 0
            if presentation:
                cv2.imshow('Frame', frame)                                                   
                cv2.waitKey(20)

# Function for sign detection thread
def sign_detection_task():    
    global distracted                                                                        
    global alarm_running
    global last_alarm_millis
    global alarm_pause
    global alarm_start_millis
    global alarm_time_to_live
    video = cv2.VideoCapture(sign_detection_video_path)                                      
    speedlimit_classification_rate = 0
    speedlimit_classification_results = []
    speedlimit_last_classification = 0
    speedlimit_active_icon = None
    speedlimit_add = False

    while video.isOpened():                                                                  
        ret, frame = video.read()
        if ret is True:
            # Adjust image gamma for better detection conditions
            frame = tools.adjust_gamma(frame, 0.7)
            results = sign_detection_model(frame)                                            
            class_dataframe = results.pandas().xyxy[0]['name']
            # Convert results to list
            result = tools.preprocess_result(class_dataframe)                                                                                                                 
            # Prepare output list which contains icons to presentation on screen
            processed_signs = tools.process_result(result, last_icon_update_time, repeats, active_images, sign_minimum_repeat, icon_time_to_live, trafficlight_pause, is_city_seen, city_signs_time_to_live)
            
            if 'speedlimit' in processed_signs:
                current_time = tools.current_milli_time()
                image_slice_with_speedlimit = tools.extract_speedlimit_sign_image_slice(results, frame)
                # If YOLO is still not sure if is it speedlimit (below repeat threshold)
                if image_slice_with_speedlimit is not None and speedlimit_classification_rate < sign_minimum_repeat and (current_time - speedlimit_last_classification) >= speed_limit_classification_pause:
                    image_slice_with_speedlimit = tools.extract_speedlimit_sign_image_slice(results, frame)
                    detected_sign = speed_limit_model.predict(image_slice_with_speedlimit)
                    speedlimit_classification_rate += 1
                    # Add classification result to list
                    speedlimit_classification_results.append(int(detected_sign[0]))
                
                # If it could be speedlimit (rate of YOLO detection is equal with threshold)
                if speedlimit_classification_rate >= sign_minimum_repeat:
                    speedlimit_classification_rate = 0
                    speedlimit_last_classification = current_time
                    # Get most common result from classification list
                    most_common_detected_sign = tools.get_most_common_result(speedlimit_classification_results)
                    most_common_sign_count = most_common_detected_sign[0][1]
                    most_common_sign = most_common_detected_sign[0][0]
                    
                    # If the same speedlimit is on classification list in most
                    if most_common_sign_count >= speed_limit_classification_confidence:
                        speedlimit_active_icon = f'speedlimit-{most_common_sign}'
                    speedlimit_classification_results.clear()
            current_time = tools.current_milli_time()
            
            if speedlimit_active_icon is not None:
                speedlimit_add = tools.check_speedlimit_deletion_timeout(speedlimit_last_classification, icon_time_to_live, current_time)
            
            if speedlimit_add is True and speedlimit_active_icon not in processed_signs:
                processed_signs.append(speedlimit_active_icon)
            
            else:
                speedlimit_active_icon = None
            # Check if app should raise alarm
            alarm = tools.alarm_needed(processed_signs, distracted)

            # Raising and shutting down alarm timers
            if alarm == True and (current_time - last_alarm_millis) >= alarm_pause and not alarm_running:
                screen.raise_alarm()   
                alarm_running = True  
                alarm_start_millis = current_time  
            if alarm_running and (current_time - alarm_start_millis) >= alarm_time_to_live:
                screen.end_alarm()
                alarm_running = False
                last_alarm_millis = current_time
            # Show images on screen    
            screen.refresh_icons(processed_signs)
            cv2.imshow('Frame2', frame)
            cv2.waitKey(20)


t1 = Thread(target = distracted_task)
t2 = Thread(target = sign_detection_task)

t1.start()  
t2.start()
#Function calls for presentation purposes
#screen.refresh_icons(['crosswalk'])   
#screen.raise_alarm()
root.mainloop()






