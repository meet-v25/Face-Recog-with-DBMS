# Imports
import PySimpleGUI as GUI, cv2 as cv, os, Stage0_Cleanup_Initiation as S0P; 
from pandas import DataFrame as pd_DataFrame, read_excel as pd_read_excel, concat as pd_concat; 
from shutil import rmtree as shutil_rmtree; 
from time import sleep as time_sleep; 


# These two lines are to recreate temp-folder to erase its previous data
if(os.path.isdir(S0P.temp_dir_path)): shutil_rmtree(S0P.temp_dir_path); 
os.mkdir(S0P.temp_dir_path); 

capture_delay = 0.25;       # in seconds ; to control face capture rate
img_count = 0; 

print('''\nStarting taking pictures. 
Please look at the camera. 
Tilt your face in different directions and give some mild expressions.\n'''); 
time_sleep(3); 
video_cap = cv.VideoCapture(0,cv.CAP_DSHOW); 




while(True):
    ret_val, img_frame = video_cap.read();                                  # Read each frame
    img_frame = cv.flip(img_frame,1,0);                                     # Mirror the frame
    gray_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY);                 # Convert to black&white
    img_resized_frame = cv.resize(gray_frame, ((S0P.img_width)//(S0P.size),(S0P.img_height)//(S0P.size)));              # Resize to save memory
    faces = S0P.face_cascade.detectMultiScale(img_resized_frame, scaleFactor=S0P.scale_factor); faces = sorted(faces, key=lambda x:x[3]); 
    # Above line detects face's coordinates, using "HAAR-Cascade"

    if(faces):
        img_count+=1
        (x,y,w,h) = [i*(S0P.size) for i in faces[0]];                       # Extract face coordinates 
        face = gray_frame[y:y+h,x:x+w];                                     # Extract face
        face_resized = cv.resize(face, ((S0P.img_width)//(S0P.size),(S0P.img_height)//(S0P.size)));                     # Resize
        
        cv.imwrite('%s/%s.png' % (S0P.temp_dir_path, ( '0'*(2-len(str(img_count)))+str(img_count) )), face_resized);    # Save images in the folder
        cv.rectangle(img_frame, (x,y), (x+w,y+h), (0,0,0), 2);              # Draw rectangle around face
        cv.imshow('WINDOW NAME', img_frame);                                # Show frame with rectangle
        time_sleep(capture_delay);                                          # Adjust capturing duration to accomodate different angles of viewer


    ### Database File & Information Related Section - Begins
    if(img_count>=S0P.image_count):
        video_cap.release(); cv.destroyAllWindows();                        # Close all OpenCV windows

        New_Record_Dict={}; j=0;                                            # Dict will contain column-header:entry pairs  &  j=iterable
        df = pd_read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); 
        excel_cols = df.columns;                                            # Store its columns headers
        max_col_len = max(len(col) for col in excel_cols);                  # To be used in API

        # Defining Layout to display Info-Taking API
        layout = list([[GUI.Text(f'Enter {col} :'+' '*(max_col_len-len(col))), GUI.InputText()]] for col in excel_cols) + [[GUI.Submit(), GUI.Cancel()]] ; 
        event, values = GUI.Window('Enter Information', layout, auto_size_text=True, default_element_size=(40,1)).Read();  # Initiate the API
        person_name = values[0]; person_rollno = values[1];                 # Extract info to give name to the folder
        
        # When we click on Submit button, Give name to the folder & Insert its record in database file
        if(event=='Submit'):
            try: os.rename(S0P.temp_dir_path, os.path.join(S0P.dir_name, person_rollno+' '+person_name));        # Save images in folder with name
            except: print("\nA folder with the same credentials already exists. Please delete it and Do this again.")

            for col in excel_cols:                                          # | For each column header, |
                try: New_Record_Dict[col] = [float(values[j])]; j+=1;       # |     insert/write a      |
                except: New_Record_Dict[col] = [values[j]]; j+=1;           # |   corresponding entry   |
            
            df = pd_concat([df, pd_DataFrame(New_Record_Dict)]);            # Concatenate both df's
            df.reset_index(inplace=True, drop=True); df.index+=1;           # To start indexing from 1
            df.to_excel(S0P.file_name, sheet_name=S0P.sheet_name);          # Write all the data to excel file

        break; 
    ### Database File & Information Related Section - Ends


    if((cv.waitKey(S0P.key_press_delay) == 27)): break;     # Stop the program if ESC key is pressed, or CLOSE button is clicked



print(str(img_count) + " number of images are taken. They are stored at : '" + os.path.join(S0P.dir_name,person_rollno + ' ' + person_name + "' location.")); 
print("The corresponding record for ", person_name, " with roll number ", person_rollno, " is added to the database file ", S0P.file_name, "."); 

exit=input("\nClick on Close(X) button of the Program-Execution window to exit.\n"); 
