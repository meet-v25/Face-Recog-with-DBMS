# Imports
from cv2 import CascadeClassifier as cv_CascadeClassifier; 
from pandas import DataFrame as pd_DataFrame; 
from os import path as os_path, mkdir as os_mkdir; 



# Initializations of variables and functions to be used in this as well as other files

dir_name       = 'Raw_Image_Data';              # Folder name in which we want to store everyone's raw data
temp_dir_name  = '@deletable_temp';             # Folder in which raw data of current scan gets tempraritly stored
temp_dir_path  = os_path.join(dir_name, temp_dir_name); 
file_name      = 'Records_Database.xlsx';       # Microsoft Excel file in which whole "Data" is stored
sheet_name     = 'Records';                     # Excel Sheet's name in the above file

size = 4;               # Image Size reduction (dividing) factor
img_width = 640;        # Size of image to be stored as raw data
img_height = 480;       # Size of image to be stored as raw data
image_count = 40;       # Total number of images per person to be saved as raw data for training

key_press_delay = 7;    # in milli seconds ; required to exit in case of emergency
scale_factor = 1.05;    # For "detectMulti" function



''' From the following 3 lines, keep only 1 line uncommented, whose HAAR-classifier you want to use '''
face_cascade = cv_CascadeClassifier('haarcascade_frontalface_alt2.xml'); max_face_error = 60;             # This may give best results
# face_cascade = cv_CascadeClassifier('haarcascade_frontalface_alt.xml'); max_face_error = 55; 
# face_cascade = cv_CascadeClassifier('haarcascade_frontalface_default.xml'); max_face_error = 55; 
''' The max_face_error is the looseness you can allow to assign a face, Must be kept in [40,100] range. '''



if(not os_path.isdir(dir_name)): os_mkdir(dir_name);            # Create main folder
if(not os_path.isfile(file_name)):                              # Create main file
    Exl_Entry = {'Name':[], 'Roll_No':[]};                      # Dict, this will be written to the excel file
    df = pd_DataFrame(Exl_Entry); df.to_excel(file_name, sheet_name=sheet_name); 


def is_yes(x): return (x=='y' or x=='Y' or x=='yes' or x=='Yes' or x=='YES'); 
