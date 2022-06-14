import time
import cv2
import numpy as np
from collections import Counter

# Function which returns current time in milliseconds
def current_milli_time():
    return round(time.time() * 1000)

def process_result(dataframe, last_icon_update_time, repeats, active_images, sign_minimum_repeat, icon_time_to_live, trafficlight_pause, is_city_seen, city_signs_time_to_live):
    '''                                               
    # Function prepares list which contain name of icons to show on screen. 
    # :dataframe : yolo detections in pandas format
    # :last_icon_update_time : dictionary with last icons update - to avoid icon-spam
    # :repeats : dictionary with number of repeats every icon
    # :active_images : current images on screen
    # :sign_minimum_repeat : minimum threshold for amount of sign detection cases to show them on screen
    # :icon_time_to_live : in milliseconds - how long icon should be on screen
    # :trafficlight_pause : time in millis between reaction on traffic lights
    # :is_city_seen : is car in built-up area
    # :city_sins_time_to_live : built-up area area time to live on screen
    '''
    icons_to_show = []
    current_time = current_milli_time()
    for item in dataframe:
        repeats[item] = repeats.get(item) + 1
        current_class_repeats = repeats.get(item)
        if item == 'trafficlight':
            if current_class_repeats >= sign_minimum_repeat:
                if (current_time - last_icon_update_time[item]) >= trafficlight_pause:
                    last_icon_update_time[item] = current_time
                    if item not in icons_to_show:
                        repeats[item] = 0
                        icons_to_show.append(item)
                        active_images[item] = True
        
        elif item == 'city-enter':
            if(current_class_repeats >= sign_minimum_repeat):
                if current_time - last_icon_update_time[item] >= city_signs_time_to_live:
                    last_icon_update_time[item] = current_time
                    if item not in icons_to_show:
                        repeats[item] = 0
                        icons_to_show.append(item)
                        active_images[item] = True
                if is_city_seen == False:
                    is_city_seen = True
                if 'city-exit' in active_images:
                    active_images.remove('city-exit')
                    repeats['city-exit'] = 0

        elif item == 'city-exit':
            if(current_class_repeats >= sign_minimum_repeat):
                if current_time - last_icon_update_time[item] >= city_signs_time_to_live:
                    last_icon_update_time[item] = current_time
                    if item not in icons_to_show:
                        repeats[item] = 0
                        icons_to_show.append(item)
                        active_images[item] = True
                if is_city_seen == True:
                    is_city_seen = False
                if 'city-enter' in active_images:
                    active_images.remove('city-enter')
                    repeats['city-enter'] = 0
        elif item == 'speedlimit':
             if(current_class_repeats >= sign_minimum_repeat):
                if current_time - last_icon_update_time[item] >= icon_time_to_live:
                    last_icon_update_time[item] = current_time
                    if item not in icons_to_show:
                        repeats[item] = 0
                        icons_to_show.append(item)
                        active_images[item] = True
        else:
            if(current_class_repeats >= sign_minimum_repeat):
                last_icon_update_time[item] = current_time
                if item not in icons_to_show:
                    repeats[item] = 0
                    icons_to_show.append(item)
                    active_images[item] = True
        
    for item in active_images:
        if active_images.get(item) == True:
            # If time to live of icon is end
            if (current_time - last_icon_update_time.get(item)) >= icon_time_to_live:
                active_images[item] = False
                repeats[item] = 0
            else:
                if item not in icons_to_show:
                    icons_to_show.append(item)
                    repeats[item] = 0

    return icons_to_show

# Convert yolo detections into list. This function is for future-development
def preprocess_result(result):
    detected_signs = []
    for item in result:
        detected_signs.append(item)
    return detected_signs

# Check if alarm is needed. Function get result of yolo detection and flag witch information if driver is distracted
def alarm_needed(result, driver_distracted):
    if ('trafficlight' in result or 'crosswalk' in result or 'stop' in result or 'equal' in result) and driver_distracted == True:
        return True

# Extract piece of frame which contains traffic sign
def extract_speedlimit_sign_image_slice(results, frame):
    xmin = results.pandas().xyxy[0]['xmin']
    xmax = results.pandas().xyxy[0]['xmax']
    ymin = results.pandas().xyxy[0]['ymin']
    ymax = results.pandas().xyxy[0]['ymax']
    image = None
    if len(xmin) > 0 and len(xmax) > 0 and len(ymin) > 0 and len(ymax) > 0:
        image = frame[ymin[0].astype(np.int):ymax[0].astype(np.int), xmin[0].astype(np.int):xmax[0].astype(np.int)]
        image = cv2.resize(image, (50, 50))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = np.asarray(image)
        return image
    return image

# Get most common result of speed-limit classifications
def get_most_common_result(detected_signs_list):
    counter = Counter(detected_signs_list)
    return counter.most_common(1)

# Check if speedlimit should be on screen or not
def check_speedlimit_deletion_timeout(speedlimit_last_classification, icon_time_to_live, current_time):
    if (current_time - speedlimit_last_classification) < icon_time_to_live:
        return True
    else:
        return False

# Adjust gamma of image
def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)


