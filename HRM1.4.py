import pandas as pd
import numpy as np
import time 

curr_clock = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime()) 

#it will read the files in different formats
def readfile(s):
    a=s.split('.')
    if(a[-1]=='xlsx'):
        return pd.read_excel(s)
    elif(a[-1]=='csv'):
        return pd.read_csv(s)
    elif(a[-1]=='json'):
        return pd.read_json(s)
    else:
        print("give the file format in xlsx/csv/json")
        return False


#returns eligible list based on certain cut-off criteria   
def cut_off(n,l):
    x1=l["Tenth Mark"]<10
    x2=l["Tenth Mark"]>n/10
    y1=l["Twelfth Mark"]>n
    y2=l["Twelfth Mark"]<100
    z1=l["Ug Mark"]>n/10
    z2=l["Ug Mark"]<10
    k=l.where(x1 & x2 & y1 & y2 & z1 & z2)
    return k


#returns total time slots with the hlep of timing provided
def time_slot_in_a_day(start,break_start,break_end,end,start_day_date_of_interview,final_eligible_list,interviewer_data):
    number_of_time_slots_per_day=np.concatenate((np.arange(start,break_start),np.arange(break_end,end)))
    x=np.ceil(final_eligible_list.shape[0]/(interviewer_data.shape[0]*number_of_time_slots_per_day.shape[0]))
    days=np.arange(start_day_date_of_interview,start_day_date_of_interview+x)
    total_time_slots=[str(i)+' - '+str(j) for i in days for j in number_of_time_slots_per_day]
    return total_time_slots

#returns final interview slots 
def finalinterviewslots(final_eligible_list,total_time_slots,interviewer_data):
    ids_of_applicates=np.array(final_eligible_list.index)

    #if the series didn't have ability to reshape then we add some dummy applicates
    dummy_applicates=np.array(['NA']*abs(final_eligible_list.shape[0]-(len(total_time_slots)*interviewer_data.shape[0])))
    
    if(ids_of_applicates.shape[0]!=len(total_time_slots)*interviewer_data.shape[0]):
        ids_of_applicates=np.concatenate((ids_of_applicates,dummy_applicates))
    newapplicate_data=ids_of_applicates.reshape(len(total_time_slots),interviewer_data.shape[0])
    
    return pd.DataFrame(newapplicate_data,index=total_time_slots)

#check of admin login
def check_admin_login(login_id,password):
    l=[('ravi@gmail.com','123456789'),('teja@gmail.com','123456789'),('ram@gmail.com','123456789')]
    if((login_id,password) in l):
        return True
    else:
        return False
def check_interviewer_login(login_id,password,name):
    l=['ravi','ram','vijay']
    if(name in l):
        return True
    else:
        return False
    
persons_logined=[]
    

def admin_login(login_id,password):
    x=0
    while(True):
        x=int(input(" press 1 to add the data\n press 2 for checking interview slots\n press 3 for checking all apllication details\n press 4 for checking details of specific student\n press 5 for see the login details of different persons\n press 6 to see number of students not attended interview\n press 7 for signout\n"))
        if(x==1):
            print("Add Applicate Data")
            #add the applicate data
            applicate_data=readfile(input("Enter file name with extension :"))
            applicate_datashape=applicate_data.shape
            applicate_data.dropna(inplace=True)
            applicate_data.drop_duplicates(inplace=True)
            applicate_data['interview status']=pd.Series(['Not peformed']*applicate_datashape[0])
            applicate_data['interview done by']=pd.Series(['Not performed']*applicate_datashape[0])
            
            print("Add Interviewer Data")
            #add the interviewer data
            interviewer_data=readfile(input("Enter file name with extension :"))
            interviewer_data.dropna(inplace=True)
            interviewer_data.drop_duplicates(inplace=True)
            interviewer_data.to_csv("interviewer_data.csv")
        
            #add starting time ending time break time and date when interviews starts
            final_eligible_list=cut_off(int(input("Enter cut_off Percentage")),applicate_data)
            final_eligible_list.dropna(inplace=True)
            final_eligible_list.to_csv("final_eligible_list.csv")
            start,break_start,break_end,end=map(float,input("Enter start,break_start,break_end,end in a row :").split())
            start_day_date_of_interview=int(input("Enter interview starting date :"))
            total_number_of_time_slots=time_slot_in_a_day(start,break_start,break_end,end,start_day_date_of_interview,final_eligible_list,interviewer_data)
            
            

        elif(x==2):
                
            #interview slot details

            x1=finalinterviewslots(final_eligible_list,total_number_of_time_slots,interviewer_data)
            print(x1)
            x1.to_csv("finalinterviewslots.csv")
            print(x)

        elif(x==3):
            #check all eligible student details
            print(final_eligible_list)

        elif(x==4):
            #check details of specific student
            student_id=int(input("Enter student ID"))
            print(final_eligible_list.loc[student_id,:])

        elif(x==5):
            print(persons_logined)
        
        elif(x==6):
            students_not_attended_interview=final_eligible_list['interview status'].value_counts(ascending=True)
            print("students not attended interview",students_not_attended_interview['Not peformed'])

        elif(x==7):
            break

def interviewer_login(name):
    x=0
    while(True):
        x=int(input("press 1 for changing the interview status\n press 2 for checking the interview status of specific student\n press 3 for checking complete details of student\n press 4 to see Number of students under him/her\n press 5 for log out\n"))
        try:
            final_eligible_list=final_eligible_list
        except:
            final_eligible_list=readfile("final_eligible_list.csv")
        try:
            interviewer_data=interviewer_data
        except:
            interviewer_data=readfile("interviewer_data.csv")

        if(x==1):
            #Modifying status of the interview
            student_id=int(input("Enter Student ID"))
            status=input("Enter Finish or Comment out")
            final_eligible_list["interview status"][student_id]=status
            final_eligible_list.to_csv("final_eligible_list.csv")

        elif(x==2):
            #check interview status of specific student
            student_id2=int(input("Enter student ID"))
            print(final_eligible_list["interview status"][student_id2])

        elif(x==3):
            # Check details of specific student
            student_id=int(input("Enter student ID"))
            print(final_eligible_list.loc[student_id,:])
        
        elif(x==4):
            #Number of students under him/her
            x1=finalinterviewslots(final_eligible_list,total_number_of_time_slots)
            print(list(x1[name]))
            
        elif(x==5):
            break
        
while(True):
    x=int(input(" press 1 for admin login\n press 2 for interviewer login\n"))
    if(x==1):
        while(True):
            #admin login
            login_id=input("Enter user id :")
            password=input("Enter Password :")     
            curr_clock = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime())
            if check_admin_login(login_id,password):
                persons_logined.append((login_id,curr_clock))
                admin_login(login_id,password)
                break
            else:
                print("Wrong details")
                
    elif(x==2):
        while(True):
            #interviewer login
            name=input("Enter Name :")          
            login_id=input("Enter user id :")
            password=input("Enter Password :")
            curr_clock = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime())           
            if check_interviewer_login(login_id,password,name):
                persons_logined.append((login_id,curr_clock))
                interviewer_login(name)
                break
            else:
                print("Wrong details")
                        
    else:
        break
