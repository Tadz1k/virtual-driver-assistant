from tkinter import *
import tkinter #Tcl/Tk GUI toolkit
from PIL import ImageTk, Image
from tools import current_milli_time

root = Tk()
image_jump_right = 95
# Pathes of sign icons
images_pathes = {'equal' : 'sign_icons/equal.jpg', 'city-enter' : 'sign_icons/city-enter.jpg', 
'stop' : 'sign_icons/stop.jpg', 'crosswalk' : 'sign_icons/crosswalk.jpg',
'speed-control' : 'sign_icons/speedcheck.jpg', 'city-exit' : 'sign_icons/city-exit.jpg',
'speedlimit-20': 'sign_icons/speedlimit-20.jpg', 'speedlimit-30': 'sign_icons/speedlimit-30.jpg', 'speedlimit-40': 'sign_icons/speedlimit-40.jpg',
'speedlimit-50': 'sign_icons/speedlimit-50.jpg', 'speedlimit-60': 'sign_icons/speedlimit-60.jpg', 'speedlimit-70': 'sign_icons/speedlimit-70.jpg',
'speedlimit-80': 'sign_icons/speedlimit-80.jpg', 'speedlimit-100': 'sign_icons/speedlimit-100.jpg', 'speedlimit-120': 'sign_icons/speedlimit-120.jpg'}
images = {}

for key in images_pathes:
    images[key] = ImageTk.PhotoImage(Image.open(images_pathes.get(key)))

active_images = {'equal' : False, 'speedlimit' : False, 'city-enter' : False, 'stop' : False,
'crosswalk' : False, 'speed-control' : False, 'city-exit' : False}

possible_speed_limit = ['speedlimit-20', 'speedlimit-30', 'speedlimit-40', 'speedlimit-50', 'speedlimit-60', 'speedlimit-70', 'speedlimit-80', 'speedlimit-100', 'speedlimit-120']



def set_screen(dim):
    root.geometry(dim)
    root.overrideredirect(1) # Hide titlebar
    root.configure(bg="white")
    return root

# Show actual images on screen
def refresh_icons(icons):
    icons.sort()
    current_image_pos_x = 0
    speedlimit_in_icon_set = [element for element in icons if(element in possible_speed_limit)]
    is_speedlimit_in_set = bool(speedlimit_in_icon_set)
    
    for element in root.winfo_children():
        element.destroy()
    if is_speedlimit_in_set:
        image = images.get(speedlimit_in_icon_set[0])
        speedlimit_label = Label(root, image = image)
        speedlimit_label.place(x=current_image_pos_x, y=0)
        speedlimit_label.image = image
        current_image_pos_x+=image_jump_right
    if 'crosswalk' in icons:
        image = images.get('crosswalk')
        crosswalk_label = Label(root, image = image)
        crosswalk_label.place(x=current_image_pos_x, y=0)
        crosswalk_label.image = image
        current_image_pos_x+=image_jump_right
    if 'equal' in icons:
        image = images.get('equal')
        equal_label = Label(root, image = image)
        equal_label.place(x=current_image_pos_x, y=0)
        equal_label.image = image
        current_image_pos_x+=image_jump_right
    if 'stop' in icons:
        image = images.get('stop')
        city_exit_label = Label(root, image = image)
        city_exit_label.place(x=current_image_pos_x, y=0)
        city_exit_label.image = image
        current_image_pos_x+=image_jump_right
    if 'speed-control' in icons:
        image = images.get('speed-control')
        speed_control_label = Label(root, image = image)
        speed_control_label.place(x=current_image_pos_x, y=0)
        speed_control_label.image = image
        current_image_pos_x+=image_jump_right
    if 'city-enter' in icons:
        image = images.get('city-exit')
        city_enter_label = Label(root, image = image)
        city_enter_label.place(x=0, y=95)
        city_enter_label.image = image
    if 'city-enter' in icons:
        image = images.get('city-enter')
        city_exit_label = Label(root, image = image)
        city_exit_label.place(x=0, y=95)
        city_exit_label.image = image

# Raising alarm on screen     
def raise_alarm():
    for x in range(15):
        print('ALARM! NIEBEZPIECZNA SYTUACJA!')
    root.configure(bg="red")

# Ending alarm on screen
def end_alarm():
    root.configure(bg="white")

        













