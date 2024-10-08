# Imports
import cv2 as cv, os, pickle, Stage0_Cleanup_Initiation as S0P; 
from shutil import rmtree as shutil_rmtree; 
from numpy import array as nparray; 

# Remove temporary directory as it shouldn't count in training
temp_dir_name = os.path.join(S0P.dir_name,S0P.temp_dir_name); 
if(os.path.isdir(temp_dir_name)): shutil_rmtree(S0P.temp_dir_path); 

# Following line : Respectively stores : Images, Labels/ids, related former two, Index of current person
x_trains=[]; y_labels=[]; hash_map={}; curr_id=0;       
print("\nStaring Training!"); 



for root,dirs,files in os.walk(S0P.dir_name):           # For every subfolder in main-database-folder
    for subdir in dirs:                                 # Extract its path in this program
        curr_id += 1; 
        hash_map[curr_id] = subdir; 
        person_path = os.path.join(S0P.dir_name,subdir); 

        for file in os.listdir(person_path):            # Using that path, For every image file in that subfolder
            if(file.endswith("png")):                   # Append the image and a new lable in respective arrays
                img_path = os.path.join(person_path,file); label = curr_id; 
                x_trains.append(cv.imread(img_path,0)); y_labels.append(int(label)); 



trained_model = cv.face.LBPHFaceRecognizer_create();                # Creating to train the model
trained_model.train(nparray(x_trains), nparray(y_labels));          # Training the model
trained_model.save("Trained_Model.yml");                            # Saving the trained model
with open("labels.pickle", 'wb') as f: pickle.dump(hash_map,f);     # Saving data for trained model

os.mkdir(temp_dir_name); 
exit=input("\nClick on Close(X) button of the Program-Execution window to exit.\n"); 
