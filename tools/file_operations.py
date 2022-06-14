from cmath import sin
import os
import cv2
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import shutil

annotations_path = ''
images_path = ''
tagname = 'speedlimit'
possible_tags = ['crosswalk', 'trafficlight', 'stop', 'speed-control', 'speedlimit']
new_tags = ['stop', 'speedlimit-40', 'city-enter', 'speedlimit-70', 'trafficlight', 'crosswalk', 'speedlimit-30', 'speedlimit-50', 'speed-control', 'city-exit', 'speedlimit-60', 'speedlimit-20', 'speedlimit-80']
roboflow = 'C:\\your\\path' #Pascal VOC format annotations path
yolo_anotations = 'C:\\your\\path' #Yolo format annotations path

def to_yolo_format():
    for item in os.listdir(annotations_path):
        single_yolo_content = ''
        file = open(f'{annotations_path}\\{item}')
        data = file.read() #Load label to variable
        bs_data = BeautifulSoup(data, "xml") #Parse xml content
        b_names = bs_data.find_all('name')
        b_xmins = bs_data.find_all('xmin')
        b_xmaxs = bs_data.find_all('xmax')
        b_ymins = bs_data.find_all('ymin')
        b_ymaxs = bs_data.find_all('ymax')
        b_width = bs_data.find('width')
        b_height = bs_data.find('height')
        first = True

        # Save properties to yolo format annotation file
        for object_index in range(len(b_names)):
            yolo_x = (int(b_xmins[object_index].text) + int(b_xmaxs[object_index].text))/(2*int(b_width.text))
            yolo_y = (int(b_ymins[object_index].text) + int(b_ymaxs[object_index].text))/(2*int(b_height.text))
            yolo_w = (int(b_xmaxs[object_index].text) - int(b_xmins[object_index].text))/int(b_width.text)
            yolo_h = (int(b_ymaxs[object_index].text) - int(b_ymins[object_index].text))/int(b_height.text)
            if first is True:
                single_yolo_content += f'{b_names[object_index].text} {yolo_x} {yolo_y} {yolo_w} {yolo_h}'
                first = False
            else:
                single_yolo_content += f'\n{b_names[object_index].text} {yolo_x} {yolo_y} {yolo_w} {yolo_h}'
        yolo_filename = item.replace('xml', 'txt')
        new_file = open(f'{yolo_anotations}\\{yolo_filename}', 'w')
        new_file.write(single_yolo_content)
        new_file.close()
            
        



# Convert classes
def redefine_images():
    for item in os.listdir(roboflow):
        file = open(f'{roboflow}\\{item}', 'r')
        data = file.read()
        new_data = ''
        if 'speedlimit' in data:
            for line in data.splitlines():
                if '<name>' in line and 'speedlimit-' in line:
                    line = '		<name>speedlimit</name>'
                new_data += f'{line}\n'
            file.close()
            os.remove(f'{roboflow}\\{item}')
            file = open(f'{roboflow}\\{item}', 'w')
            file.write(new_data)
            print(item)
            file.close()
        else:
            file.close()

        
def delete_images():
    for item in os.listdir('C:\\Users\Adison\Desktop\\to_assign\\train'):
        if '.png' in item or '.jpg' in item:
            os.remove(f'C:\\Users\Adison\Desktop\\to_assign\\train\\{item}')

def assign_images():
    for item in os.listdir('C:\\Users\Adison\Desktop\\to_assign\\train'):
        if '.xml' in item:
            shutil.move(f"C:\\Users\\Adison\\Desktop\\to_assign\\train\\{item}", f"C:\\Users\\Adison\\Desktop\\dataset\\annotations\\roboflow_annotations\\{item}")
        #else:
            #shutil.move(f"C:\\Users\Adison\Desktop\\to_assign\\train\\{item}", f"C:\\Users\\Adison\\Desktop\\dataset\\images\\{item}")


def unique_tags():
    unique_tags = []
    for item in os.listdir(roboflow):
        current_file = open(f'{roboflow}\\{item}', 'r') #Read file
        data = current_file.read() #Load file content into variable
        bs_data = BeautifulSoup(data, "xml") #Parse xml format
        b_objects = bs_data.find_all('name') #Search objects with tag 'name'
        for obj in b_objects:
            if obj.text not in unique_tags:
                unique_tags.append(obj.text)
    return unique_tags


def replace_annotations():
    for item in os.listdir(annotations_path): #Iteration over all annotation files
        current_file = open(f'{annotations_path}\\{item}', 'r')
        data = current_file.read()
        if tagname in data:
            bs_data = BeautifulSoup(data, "xml") #Parse xml file
            b_objects = bs_data.find_all('object') #Serach objects with tag 'object'
            b_xmins = bs_data.find_all('xmin')
            b_xmaxs = bs_data.find_all('xmax')
            b_ymins = bs_data.find_all('ymin')
            b_ymaxs = bs_data.find_all('ymax')
            b_labels = bs_data.find_all('name')
            tag_names = []
            if os.path.exists(f'{images_path}\\{item.replace(".xml", ".png")}'): image_name = item.replace('.xml', '.png') #Check if file exists
            else: image_name = item.replace('.xml', '.jpg') 
            for object_index in range(len(b_objects)): #Iterate over object in annotate file. They are identified by b_objects list order.
                image = cv2.imread(f'{images_path}\\{image_name}')
                rec_start_point = (int(b_xmins[object_index].text), int(b_ymins[object_index].text)) #Rectangle starting point
                rec_end_point = (int(b_xmaxs[object_index].text), int(b_ymaxs[object_index].text)) #Rectangle end point
                cv2.rectangle(image, rec_start_point, rec_end_point, (255, 0, 0), 2)
                plt.ion() #interactive mode
                plt.title(item) 
                plt.imshow(image)
                print('Wpisz nazwę taga')
                tag = input() #Input new tag for labeled object
                if tag not in new_tags:
                    tag = 'delete'
                print(tag)
                tag_names.append(tag) #Add new tag
                current_file.close()

            new_annotation_file = '' #Annotation file content container
            object_seq_num = 0 
            for line in data.splitlines():
                if f'<name>' in line and '</name>' in line:
                    line = f'        <name>{tag_names[object_seq_num]}</name>' #Replace name
                    object_seq_num += 1
                if '</annotation>' in line: new_annotation_file += line
                else: new_annotation_file += f'{line}\n'

            os.remove(f'{annotations_path}\\{item}') #Remove old annotation file
            new_file = open(f'{annotations_path}\\{item}', 'w') #Create new annotation file
            new_file.write(new_annotation_file) #Write content into new file
            new_file.close()


#replace_annotations()
#redefine_images()
#assign_images()
#delete_images()
to_yolo_format()