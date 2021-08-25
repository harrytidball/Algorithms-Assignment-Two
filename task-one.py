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
This function is used to put all the patient information
that need to be displayed into a list. The information
can then be manipulated more easily.
"""
def createPatientInfo(patient_condition):
    for x in range(len(patient_name)):
        if condition[x] == patient_condition:
            patient_info.append("Patient name: " + patient_name[x] + " Age: " + str(age[x]) + " BMI: " + bmi[x] + " Weight Classification: " + condition[x])
    return patient_info

"""
This function appends the first 5 patients into
a list of indices.
"""
def sortWorstPatients(bmi_list, bmi, worst_index):
    for x in range(5):
        worst_index.append(bmi.index(bmi_list[x]))
    return worst_index

"""
This function separates the data into a list containing
males and a list containing females.
"""
def sortBySex(sex, index_list, sorted_list_male, sorted_list_female):
    for x in range(len(index_list)):
        if sex[index_list[x]] == "M":
            sorted_list_male.append(index_list[x])
        elif sex[index_list[x]] == "F":
            sorted_list_female.append(index_list[x])
    return sorted_list_male, sorted_list_female

"""
This function prints the worst patients and creates
a link break after every 10 patients.
"""
def displayWorstPatients(body_type, sex, list):
    print("\nWorst " + body_type + " " + sex + " Patients:")
    for x in range(len(list)):
        print("Patient name: " + patient_name[list[x]] + " Age: " + str(age[list[x]]) + " BMI: " + bmi[list[x]] + " Weight Classification: " + condition[list[x]])

"""
This function calculates the patient's age using
their date of birth and the datetime function.
"""
def calculateAge(born): 
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

#Create list of patients
patient_name = sortData(data, "patient_name", 0, 1)
patient_name = flattenList(patient_name)

#Create list of dates of birth
dob = sortData(data, "dob", 1, 2)
dob = flattenList(dob)

age = []

#Call calculateAge function to add ages of patients to age list
for x in range(len(dob)):
    calculateAge(date(int((dob[x])[6:10]), int((dob[x])[3:5]), int((dob[x])[0:2])))

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

#For each weight class, create list of patient data
patient_info = createPatientInfo("Obese")
patient_info = createPatientInfo("Underweight")
patient_info = createPatientInfo("Overweight")
patient_info = createPatientInfo("Normal")

#Print the patient data and create a link break after every 10 patients.
for x in range(len(patient_info)):
    if x % 10 == 0 and x != 0:
        print("\n" + patient_info[x])
    else:
        print(patient_info[x])

worst_underweight = []
worst_obese = []

worst_underweight_male = []
worst_underweight_female = []

worst_obese_male = []
worst_obese_female = []

#Create copies of lists for data manipulation
sorted_obese = bmi.copy()
sorted_underweight = bmi.copy()

#Sort respective lists in descending and ascending order
sorted_obese.sort(reverse=True)
sorted_underweight.sort()

index_obese = []
index_underweight = []

#Get the indices of the worst patients for each necessary weight class
index_obese = sortWorstPatients(sorted_obese, bmi, index_obese)
index_underweight = sortWorstPatients(sorted_underweight, bmi, index_underweight)

#Sort the worst patients to into male and female
sortBySex(sex, index_obese, worst_obese_male, worst_obese_female)
sortBySex(sex, index_underweight, worst_underweight_male, worst_underweight_female)

#Print the worst patients
displayWorstPatients("Obese", "Male", worst_obese_male)
displayWorstPatients("Obese", "Female", worst_obese_female)
displayWorstPatients("Underweight", "Male", worst_underweight_male)
displayWorstPatients("Underweight", "Female", worst_underweight_female)