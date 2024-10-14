# Imports
import PySimpleGUI as GUI, pandas as pd, Stage0_Cleanup_Initiation as S0P; 
from shutil import rmtree as shutil_rmtree; 
from numpy import nan as NaN; 
from os import path as OSpath; 



# To add columns with their headers, and also its data at will
def Insert_Cols():

    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); df_rows = len(df.index); 
    new_cols_dict={}; new_cols_lst=[];      # Dict to store pairs col_name:[col_vals]    &   corresponding col_names are in list

    print("\nYou can add Columns only. Manual Row-addition idds not allowed for data-conservation purpose."); 
    print("\nCurrent dataset in excel has the following columns : "); 
    for i in list(df.columns): print(f'< {i} >', end='  '); 
    print(); 

    while(True):
        try: n = int(input("\nEnter the 'Number' of columns you want to add : ")); print(); break; 
        except ValueError: closed = input("\nYou did not enter a number. Please enter a +ve interger. Press Enter to continue."); continue; 
    
    for i in range(1,1+n):
        new_col_name = input(f'Enter {i}th new column name : '); 
        new_cols_dict[new_col_name] = [NaN]*df_rows; new_cols_lst.append(new_col_name); 
        # Above line, If fill_value is not entered, fill with "NaN"-"np.nan"-"Missing-Values", so that we can do operations even if it's empty.

    for i in range(1,1+n):
        choice = input(f"\nDo you want to add values for  < {new_cols_lst[i-1]} >  column? (y/n) : "); 
        if(S0P.is_yes(choice)): 
            lst=[]; print("--> If you don't have a value yet, for some records, you have to simple press Enter when those record comes.\n"); 
            for j in range(1,df_rows+1):
                temp_entry = input(f"Enter {j}th value under  < {new_cols_lst[i-1]} >  column : "); 
                try: lst.append(float(temp_entry));                         #  | Append all of the |
                except: lst.append(temp_entry);                             #  |   values in lst   |
            new_cols_dict[new_cols_lst[i-1]] = lst;                         #  Then assign lst to corresponding col_name in dict
    
    del new_cols_lst, lst; 
    choice = input("\nYou sure you want to proceed with adding all the above mentioned columns and their data into the file? (y/n) : "); 
    if(S0P.is_yes(choice)): 

        temp_df = pd.DataFrame(new_cols_dict); temp_df.index+=1;            # To start indexing from 1
        new_df = pd.concat([df,temp_df], axis=1);                           # Concatenate both df's 
        
        while(True):
            try: new_df.to_excel(S0P.file_name, sheet_name=S0P.sheet_name); break;       # Write all the data to excel file
            except PermissionError: closed = input("\nThe file is open. Please close it & press Enter to process the updates to the file."); continue; 
        print("\nColumns added and Database-Excel file updated."); 
    
    else: print("\nThis Process Aborted."); 






# Deletes the column with headers/names that you want
def Delete_Cols():
    
    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); 
    del_col_lst=[]; len_lst=0;                  # del_col_lst stores col_names to be deleted

    print("\nCurrent columns in the database are as follows : "); 
    for i in list(df.columns): print(f'< {i} >', end='    '); 
    print("\n\nEnter column names that you want to delete, each name in a new line."); 
    print("When you are done entering all of such names, press Enter key once more to proceed ahead."); 

    while(True):
        temp_col = input(f"\n(You can always press Enter to stop this)  Enter {len_lst+1}th column name : "); 
        if(temp_col==''): break;                                        # When Enter is pressed once more, loop breaks and comes out. 
        if(temp_col not in df.columns): print("--->> This column isn't in database. Please Enter a valid column name."); 
        else: del_col_lst.append(temp_col); len_lst+=1; 
    
    print("\n\nThe names of the columns that you have chosen to delete are as follows :"); 
    for i in del_col_lst: print(f'< {i} >', end='    '); 

    choice=input("\n\nYou sure you want to proceed with deleting all the above mentioned columns? (y/n) : "); 
    if(S0P.is_yes(choice)): 

        df.drop(del_col_lst, axis=1, inplace=True);                     # Deletes columns, with names in del_col_lst, from df
        while(True):
          try: df.to_excel(S0P.file_name, sheet_name=S0P.sheet_name); break; 
          except PermissionError: closed = input("\nThe file is open. Please close it & press Enter to process the updates to the file."); continue; 
        
        print("\nColumns deleted and the Databse Excel file updated."); 
    else: print("\nThis Process Aborted.");  






# Along with deleting the records from excel file, we have to delete the same folders from the "database" folder
def Folders_Delete(del_df):

    # Extract Roll-Numbers and Names of the Record we want to delete
    del_rolls = list(del_df[del_df.columns[1]]); 
    del_names = list(del_df[del_df.columns[0]]); 
    length = len(del_rolls); 

    for i in range(length):
        person_path = OSpath.join(S0P.dir_name, str(del_rolls[i])+' '+str(del_names[i]));       # Join R.N. & Name to generate folder_name
        if(OSpath.isdir(person_path)): shutil_rmtree(person_path);                              # Delete that folder and all images inside it






# Deletes the records of the students you want, with help of their roll numbers
def Delete_Rows():

    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); 
    del_roll_lst=[]; del_row_lst=[];            # del_roll_lst stores all Roll_Nos to be deleted, similarly del_row_lst for rows-indices
    
    print("\nEnter Roll-Numbers of the entries that you want to delete. Please write each roll-number, seperated by 'Space' of spacebar."); 
    print("When you are done entering all of such names, press Enter key once more to proceed ahead.\n"); 

    while(True):
        del_rolls = list(map(int,input("\n(You can always press Enter to stop this)  Enter Roll Numbers seperated by space : ").split())); 
        if(del_rolls==[]): break;               # When Enter is pressed once more, loop breaks and comes out. 
        del_roll_lst += del_rolls; 
    
    print("\n\nRoll Numbers you entered to be deleted are :", del_roll_lst); del del_rolls; 

    choice=input("\nYou sure you want to proceed with deleting all the above mentioned records? (y/n) : "); 
    if(S0P.is_yes(choice)): 

        print("\n ''' Deleting... Please give a moment... ''' "); 
        roll_lst = [0] + list(df['Roll_No'].values);                                # All the roll numbers in the dataset
        for roll in del_roll_lst: del_row_lst.append(roll_lst.index(roll));         # To extract indices of Roll-Nos, using which only we can delete
        
        del_df=pd.DataFrame(df.loc[del_row_lst,:]);                                 # Extract df to delete folders
        Folders_Delete(del_df); del del_roll_lst, del_df; 
        df.drop(del_row_lst, axis=0, inplace=True);                                 # Deletes rows, with roll-nos in del_row_lst, from df
        df.reset_index(inplace=True, drop=True); df.index+=1;                       # To start indexing from 1
        
        while(True):
          try: df.to_excel(S0P.file_name, sheet_name=S0P.sheet_name); break; 
          except PermissionError: closed = input("\nThe file is open. Please close it & press Enter to process the updates to the file."); continue; 
        
        print("\nDeletion completed. Database Excel file updated."); 
    else: print("\nThis Process Aborted.");  






# Displays which records have some missing-info, according to your will
def Locate_Remove_Missing_Values():

    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); df_rows=len(df); 
    
    # Locate Section
    choice = input("Do you want to print all row indices with Missing-Value(s) in it? (y/n) : "); 
    if(S0P.is_yes(choice)):
        nan_df_bool = pd.isnull(df.values); nan_rows=[];        # nan_df_bool Stores True/False database, True if missing value  &  nan_rows the rows with nan entries
        for i in range(df_rows):
            if(True in nan_df_bool[i]): nan_rows.append(i+1); 
        print(nan_rows); del nan_df_bool, nan_rows; 
        print("Note that the above indices are those from the first column (unnamed) of the database, and not from the excel's in-built left-index-panel."); 
        
    print("\nDo you want to print whole database to see Missing Values? Missing Values will be shown by a BLANK, this symbol -> '__________' without quotes('')."); 
    choice = input("Should we print? (y/n) : "); 
    if(S0P.is_yes(choice)): print(); print(df.replace(NaN,'__________', inplace=False));            # Replace Nan by BLANK to print


    # Remove Section
    print("\n\nDo you want to remove some/all rows with 'Missing-Values'?"); 
    print("Don't worry, you will be notified which all the entries will going be deleted, according to your choice of the method of deletion."); 
    choice = input("So, wanna delete? (y/n) : "); 
    
    if(S0P.is_yes(choice)):
        print("\n\n\nEnter an index corresponding to the Method of Deletion you want to follow, from the following list."); 
        print("\n1. Delete all rows/entries having Missing-Value in  'a Given Particular Column only'.");     print("--->>  Description  --->>   Checks from top to bottom in a given column only. If an empty cell is encountered, the row containing that cell will be deleted. This will be done for all such rows."); 
        print("\n2. Delete all rows/entries having Missing-Value in  'All Columns'.");                        print("--->>  Description  --->>   Start checking each row from top to bottom. If a row has 'ALL' the cells empty except 'Name' and 'Roll_No', that row is deleted. Hence, ALL such rows will be deleted."); 
        print("\n3. Delete all rows/entries having Missing-Value in  'Any Column'.");                         print("--->>  Description  --->>   Start checking each row from top to bottom. If a row has 'ANY' of its cells empty, that is if the row has at-least one empty cell, that row will be deleted. Hence, ALL such rows will be deleted."); 
        choice = input("\nEnter your index here : (1/2/3) : "); 

        if(choice=='1' or choice=='2' or choice=='3'):
            
            if(choice=='1'): 
                print("\nCurrent columns in the database are as follows : "); 
                for i in list(df.columns): print(f'< {i} >', end='    '); 
                print(); 
                
                while(True):
                    col_name = input("\nEnter the Column-Name that you want to delete with-respect-to : "); 
                    if(col_name==''): print("\nSince you entered nothing, exiting."); break; 
                    elif(col_name not in df.columns): closed = input("\nInvalid column name. Please repeat the process. Press Enter to continue."); continue; 
                    else:
                        nan_rows=[]; nan_rows_bool = pd.isnull(df[col_name]);           # Empty rows-indices  &  All rows nan in bool
                        for i in range(1, 1+df_rows):
                            if(nan_rows_bool[i]==True): nan_rows.append(i); 
                        print(f"\nThe indices of the entries having Missing-Values in the  < {col_name} >  column are : "); 
                        print(nan_rows); del nan_rows_bool; break; 
        

            elif(choice=='2' or choice=='3'): 
                nan_rows=[]; nan_df_bool = pd.isnull((df.values)[:,2:]);            # Empty rows-indices  &  All rows nan in bool
                
                if(choice=='2'):
                    for i in range(df_rows): 
                        if(not(False in nan_df_bool[i])): nan_rows.append(i+1); 
                if(choice=='3'):
                    for i in range(df_rows): 
                        if(True in nan_df_bool[i]): nan_rows.append(i+1); 
                
                print("\nThe indices of the entries having Missing-Value in All the columns are : "); print(nan_rows); del nan_df_bool; 
            

            delete = input("\nShould we proceed to delete all of the above-mentioned indexed rows? (y/n) : "); 
            if(S0P.is_yes(delete)): 

                del_df = pd.DataFrame(df.loc[nan_rows,:]);                  # Extract df to delete folders
                Folders_Delete(del_df); del del_df; 
                df.drop(nan_rows, axis=0, inplace=True);                    # Deletes rows, with roll-nos in del_row_lst, from df
                df.reset_index(inplace=True, drop=True); df.index+=1;       # To start indexing from 1
                
                while(True):
                  try: df.to_excel(S0P.file_name, sheet_name=S0P.sheet_name); break;        # Write all the data to excel file
                  except PermissionError: closed = input("\nThe file is open. Please close it & press Enter to process the updates to the file."); continue; 
                print("\nYour process is done. Database Excel file is updated."); 
            
            else: print("\nThis Process Aborted.");  
        else: print("The index you entered is not mentioned in the list. Please run it again to do it. No changes made."); 
    else: print("\nNo changes made to the file.")






def Search_Record():
    
    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); 
    
    while(True):
        print("\n\nCurrent columns in the database are as follows : "); 
        for i in list(df.columns): print(f'< {i} >', end='    '); 
        print('\n'); 

        while(True):
            col_name = input("\nEnter column name from above, in which you want to search : "); 
            if(col_name not in df.columns): print("--->> This column isn't in database. Please Enter a valid column name."); continue; 
            else:
                col_data = input("\nEnter the data that you want to search for : "); 
                try: col_data = float(col_data); 
                except: pass; 
                try:
                    col_index = 1 + (list(df[col_name])).index(col_data); 
                    print(f'Data found at index {col_index}.'); 
                    layout = list([[GUI.Text(f'{col} : {df[col][col_index]}')]] for col in df.columns) + [[GUI.Text(' '*80)]] ; # Defining Layout to display Info-Taking API
                    GUI.Window('Results', layout, auto_size_text=True, default_element_size=(40,1)).Read();                     # Initiate the API
                except: print("--->> Data not found under given column."); 
                break; 
        choice = input("\nDo you want to search again? (y/n) : "); 
        if(S0P.is_yes(choice)): continue; 
        else: break; 






# Displays the whole dataset stored in the Excel-Dataset file
def Display_Dataset():
    df = pd.read_excel(S0P.file_name, index_col=0, sheet_name=S0P.sheet_name); print(df); 
    print("\nEmpty-Cells are shown by 'NaN', if any."); 
    print("It means - either the data/value has not yet been entered - or it has been deleted afterwards, in those cells.")







##### Main Runner Program

print("\nYou are entering in an infinite loop!\n"); 

while(True):
    print(("\n"*3) + "Please enter an index corresponding to your choice from the following list : \n"); 

    print("1. Insert Columns.               (Estimated Time : 1x) "); 
    print("2. Delete Columns.               (Estimated Time : 1x) "); 
    print("3. Delete Rows.                  (Estimated Time : 2x) "); 
    print("4. Find/Delete Empty Cells       (Estimated Time : 3x) "); 
    print("5. Search Record                 (Estimated Time : 2x) "); 
    print("6. Display Dataset.              (Estimated Time : 1x) "); 
    print("7. Exit.                         (Estimated Time : 0x) "); 

    choice = input("\nEnter your index here : (1/2/3/4/5/6) : "); print(''); 

    if  (choice=='1'): Insert_Cols(); 
    elif(choice=='2'): Delete_Cols(); 
    elif(choice=='3'): Delete_Rows(); 
    elif(choice=='4'): Locate_Remove_Missing_Values(); 
    elif(choice=='5'): Search_Record(); 
    elif(choice=='6'): Display_Dataset(); 
    elif(choice=='7'): break; 
    else:              print("--->> Your entered index is not in the list above."); 

    Continue = input("\n--> Press Enter when you want to proceed further."); 

print('You exited successfully!\n'); 
