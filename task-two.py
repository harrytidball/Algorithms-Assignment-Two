import csv
from datetime import date
import datetime as dt

#Import data file and append to a list
with open("DADSA 2021 CWK B DATA COLLECTION.csv", newline='') as data_file:
    rows = csv.reader(data_file)
    data = []
    for row in rows:
        data.append(row)

"""
This function is used to separate the data from the file
into smaller, specific lists. Its parameters 'x' and 'y'
represent the segmentation of the data.
"""
def sortData(data, data_type, x, y):
    data_type = []
    i = -1
    for _ in data:
        i += 1
        data_type.append(data[i][x:y])
    #Remove title from list
    data_type.pop(0)
    return data_type

"""
This function is used to flatten lists from a 2D
state into 1D.
"""
def flattenList(data):
    data = [val for sublist in data for val in sublist]
    return data

"""
This function is used to put all the patient names that
need to be displayed into a list. The information
can then be manipulated more easily.
"""
def createPatientInfo(sorted_by_ages, patient_info):
    for x in range(len(sorted_by_ages)):
        patient_info.append("Patient name: " + patient_name[sorted_by_ages[x]])
    return patient_info

"""
This function calculates the patient's age using
their date of birth and the datetime function.
"""
def calculateAge(born, year, month, day): 
    today = date.today()
    try:  
        birthday = born.replace(year = today.year) 
    #If patient is born on February 29th avoid error
    except ValueError:  
        birthday = born.replace(year = today.year, 
                  month = born.month + 1, day = 1) 
    if birthday > today: 
        age.append(today.year - born.year - 1)
    else: 
        age.append(today.year - born.year)
    
    #Create age in days to decipher between patients of the same age
    age_in_days.append((today - date(year, month, day)).days)

"""
This function classifies each patient's BMI
depending on their body build and adds it 
to their record.
"""
def classifyBMI(overweight_var, obese_var, x):
    if float(bmi[x]) < 18.5:
        condition[x] = "Underweight"
    elif float(bmi[x]) >= 18.5 and float(bmi[x]) < 25:
        condition[x] = "Normal"
    elif float(bmi[x]) >= 25 and float(bmi[x]) < overweight_var:
        condition[x] = "Overweight"
    elif float(bmi[x]) > obese_var:
        condition[x] = "Obese"

"""
This function sorts the patients in descending order
based on their age. This is done by zipping the list of ages
with the list of patient indices.
"""
def sortByAge(priority_list, priority_list_ages, sorted_by_age):
    for x in range(len(priority_list)):
        priority_list_ages.append(age_in_days[priority_list[x]])
    zipped_lists = zip(priority_list_ages, priority_list)
    sorted_zipped_lists = sorted(zipped_lists, reverse=True)
    sorted_by_age = [z for _, z in sorted_zipped_lists]
    return sorted_by_age

"""
This function prints the patients and creates
a line break after every 10 patients.
"""
def displayData(patients_ordered, priority):
    print(priority + " Priority Patients:\n" + "(In order of priority)\n")
    for x in range(len(patients_ordered)):
        if x % 10 == 0 and x != 0:
            print("\n" + patients_ordered[x])
        else:
            print(patients_ordered[x])

#Create list of patients
patient_name = sortData(data, "patient_name", 0, 1)
#Flatten list from 2D to 1D
patient_name = flattenList(patient_name)

#Create list of dates of birth
dob = sortData(data, "dob", 1, 2)
dob = flattenList(dob)

age = []
age_in_days = []

#Call calculateAge function to add ages of patients to age list
for x in range(len(dob)):
    calculateAge(date(int((dob[x])[6:10]), int((dob[x])[3:5]), int((dob[x])[0:2])), 
    int((dob[x])[6:10]), int((dob[x])[3:5]), int((dob[x])[0:2]))

#Create list of sexes
sex = sortData(data, "sex", 2, 3)
sex = flattenList(sex)

#Create list of heights
height = sortData(data, "height", 3, 4)
height = flattenList(height)

#Create list of weights
weight = sortData(data, "weight", 4, 5)
weight = flattenList(weight)

#Create list of builds
body_build = sortData(data, "body_build", 5, 6)
body_build = flattenList(body_build)

#Create list of smoking data
smoker = sortData(data, "smoker", 6, 7)
smoker = flattenList(smoker)

#Create list of asthma data
asthmatic = sortData(data, "asthmatic", 7, 8)
asthmatic = flattenList(asthmatic)

#Create list of NJT/NGR data
njt_ngr = sortData(data, "njt_ngr", 8, 9)
njt_ngr = flattenList(njt_ngr)

#Create list of hypertension data
hypertension = sortData(data, "hypertension", 9, 10)
hypertension = flattenList(hypertension)

#Create list of Renal RT data
renal = sortData(data, "renal", 10, 11)
renal = flattenList(renal)

#Create list of ileostomy/colostomy data
ileostomy_colostomy = sortData(data, "ileostomy_colostomy", 11, 12)
ileostomy_colostomy = flattenList(ileostomy_colostomy)

#Create list of parenteral nutrition data
nutrition = sortData(data, "nutrition", 12, 13)
nutrition = flattenList(nutrition)

bmi = []
condition = []

#Formula for calculating BMI, for each patient calculate and add data to list
#Create null conditions values as placeholder before classifyBMI is called
for x in range(len(patient_name)):
    bmi.append("{:.1f}".format(int(weight[x]) / (float(height[x])**2))) 
    condition.append(None)

#Set parameters for each weight class depending on body build
for x in range(len(patient_name)):
    if body_build[x] == "Slim":
        classifyBMI(28, 28, x)
    elif body_build[x] == "Regular":
        classifyBMI(29, 29, x)
    elif body_build[x] == "Athletic":
        classifyBMI(30, 30, x)

patient_info = []

#Creating list of lists, containing all conditions
conditions = []
conditions.append(condition)
conditions.append(smoker)
conditions.append(asthmatic)
conditions.append(njt_ngr)
conditions.append(hypertension)
conditions.append(renal)
conditions.append(ileostomy_colostomy)
conditions.append(nutrition)

need_dietician = []

#Establishing which patients need a dietician
for x in range(len(patient_name)):
    for y in range(len(conditions)):
        #If obese then patient needs dietician
        if conditions[y][x] == "Obese":
            need_dietician.append(patient_name.index(patient_name[x]))
            break
        #If underweight then patient needs dietician
        elif conditions[y][x] == "Underweight":
            need_dietician.append(patient_name.index(patient_name[x]))
            break
        #If patient has any condition then needs dietician
        elif conditions[y][x] == "Y":
            need_dietician.append(patient_name.index(patient_name[x]))
            break

top_priority = []

conditions_counter = 0

#Calculating the amount of different types of condition in the file
no_of_conditions = sum(isinstance(i, list) for i in conditions)

#Estabilishing which patients are top priority
for x in range(len(patient_name)):
    #If asthmatic or smoker and aged over 55 patient is top priority
    if (asthmatic[x] == "Y" or smoker[x] == "Y") and age[x] > 55:
        top_priority.append(patient_name.index(patient_name[x]))
    #If obese and suffers from hypertension then patient is top priority
    elif condition[x] == "Obese" and hypertension[x] == "Y":
        top_priority.append(patient_name.index(patient_name[x]))
    else:
        for y in range(len(conditions)):
            #Calculating how many conditions each patient has, if over 2 conditions then patient is top priority
            if conditions[y][x] == "Obese" or conditions[y][x] == "Underweight" or conditions[y][x] == "Y":
                conditions_counter += 1
            if conditions_counter > 2:
                top_priority.append(patient_name.index(patient_name[x]))
                conditions_counter = 0
            if y == no_of_conditions - 1:
                conditions_counter = 0

low_priority = []

#Estabilishing which patients need dietician, but are low priority
for x in range(len(need_dietician)):
    if need_dietician[x] not in top_priority:
        low_priority.append(need_dietician[x])

top_priority_ages = []
low_priority_ages = []

top_priority_ages_sorted = []
low_priority_ages_sorted = []

#Sorting the ages of the two priority groups in descending order
top_priority_ages_sorted = sortByAge(top_priority, top_priority_ages, top_priority_ages_sorted)
low_priority_ages_sorted = sortByAge(low_priority, low_priority_ages, low_priority_ages_sorted)

top_priority_patient_info = []
low_priority_patient_info = []

#Generating the necessary data to display
top_priority_patient_info = createPatientInfo(top_priority_ages_sorted, top_priority_patient_info)
low_priority_patient_info = createPatientInfo(low_priority_ages_sorted, low_priority_patient_info)

#Display data
print("Patients who need to be referred to a dietician:\n")
displayData(top_priority_patient_info, "Top")
displayData(low_priority_patient_info, "\nLow")