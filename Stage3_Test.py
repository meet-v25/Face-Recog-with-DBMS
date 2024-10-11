# Imports
import cv2 as cv, Stage0_Cleanup_Initiation as S0P; 
from pickle import load as pickle_load; 

trained_model = cv.face.LBPHFaceRecognizer_create();    # Load model to identify a face
trained_model.read("./Trained_Model.yml"); 
   
max_face_error = S0P.max_face_error;                    # Maximum acceptable "ERROR" to correctly assign predicted face
font = cv.FONT_HERSHEY_SIMPLEX; 

labels = {};                                            # Dict for showing name of person using lable
with open("labels.pickle", 'rb') as f:                  # Load saved data 
    saved_labels = pickle_load(f); 
    labels = {k:v for k,v in saved_labels.items()}; 

choice = input("\nDo you want to display maximum acceptable face error for once? (y/n) : "); 
if(S0P.is_yes(choice)): print("Max Face Error that is acceptable =", S0P.max_face_error); 

choice = input("\nDo you want to display face-error values for each test? (y/n) : "); 
print("\nStarting the camera."); 
print("\nClick on Close-Button(X) to exit."); 

if(S0P.is_yes(choice)): print("\n\nFace Error values will be printed below : \n"); 
video_cap = cv.VideoCapture(0); 



while(True):
    ret_val, img_frame = video_cap.read(); 
    img_frame = cv.flip(img_frame,1,0); 
    gray_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2GRAY); 
    img_resized_frame = cv.resize(gray_frame, ((S0P.img_width)//(S0P.size), (S0P.img_height)//(S0P.size))); 
    faces = S0P.face_cascade.detectMultiScale(img_resized_frame,scaleFactor=S0P.scale_factor); 
    

    for (x,y,w,h) in faces: 
        (x,y,w,h) = [i*(S0P.size) for i in (x,y,w,h)];      # Locate the actual face, using resized-face's coordinates
        face = gray_frame[y:y+h, x:x+w]; 
        face_resized = cv.resize(face, ((S0P.img_width)//(S0P.size),(S0P.img_height)//(S0P.size))); 

        id_pred, pred_err = trained_model.predict(face);    # Predict identity and accuracy of prediction
        cv.rectangle(img_frame, (x,y), (x+w,y+h), (0,255,0), 2); 
        if(S0P.is_yes(choice)): print(pred_err)

        # If accuracy index is in limits, put persons names on output frame, Else put "NOT RECOGNIZED" on output frame
        if (pred_err<=max_face_error): cv.putText(img_frame, labels[id_pred],  (x-10,y-10), font, 1, (0,255,0), 2); 
        else:                          cv.putText(img_frame, 'NOT RECOGNIZED', (x-10,y-10), font, 1, (0,0,255), 3); 


    cv.imshow('WINDOW NAME',img_frame); 
    if(cv.waitKey(S0P.key_press_delay) == 27): break;           # Stop the program if ESC key is pressed, or CLOSE button is pressed

video_cap.release(); cv.destroyAllWindows(); 
exit=input("\nClick on Close(X) button of the Program-Execution window to exit.\n"); 
