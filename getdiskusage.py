# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 12:01:35 2019

@author: dell-pc
"""
#importing required modules.

import sys , os , errno , json


import psutil
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

#checking if two arguments are passed , if not exiting.

if(len(sys.argv) != 2):
    print("Usage: " + sys.argv[0] + " /directory" + " Kindly check if you have passed requiered arguments")
    sys.exit(1)

#changing the directory to the directory passed as argument
    
try:
    os.chdir(sys.argv[1])

#Catching errors if any such as when passed argument is not a directory or non-existing directory is passed or when trying to access the directory for which you dont have access.
    
except OSError as Exception:
    if (Exception.errno == errno.ENOENT):
        print(sys.argv[1] + " The entered directory does not exists")
        sys.exit(1)
        
    if (Exception.errno == errno.ENOTDIR):
        print(sys.argv[1] + " This is not a directory")
        sys.exit(1)
        
    if (Exception.errno == errno.EACCES):
        print(sys.argv[1] + " You are not authorized to access this folder")

#Creating a dictonary to list out the files with their disk usage.
        
fileList = {}

#using scandir(path) checking the entries in the directory if they are files,checking their size and adding to the list.

with os.scandir(os.getcwd()) as currentDir:
    for entries in currentDir:
        if entries.is_file():
           entries = os.path.join(os.getcwd() , entries)
           fileList[entries] = os.lstat(entries).st_size
            
#Printing the output in json format.
           
print (json.dumps({"files" : fileList} , indent=4))
print("------------------------------------------------------------")
#Writing output to a txt file





"""json.dump(fileList , open("FileDetails.txt",'w'))

FileModTime = {}

with os.scandir(os.getcwd()) as CurrentDirectory:
    for files in CurrentDirectory:
        if files.is_file():
            files = os.path.join(os.getcwd() , files)
            FileModTime[files] = os.lstat(files).st_ctime
            print(FileModTime) """

## Output is in csv file which will be created in the path which is given as argument

with open('output.csv' , 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key , value in fileList.items():
        writer.writerow([key , value])
        
print ("Output is written to output.csv file")
print("------------------------------------------------------------")
#Printing the File with Max size 

maxValue = max(fileList.items() , key=lambda k: k[1])
print("This file is taking the maximum space in the directory ")
print(maxValue)
print("------------------------------------------------------------")

print("File with max size has been written to FileWithMaxSize.txt which is created at  " + sys.argv[1] + " location" )

print("------------------------------------------------------------")

#Writing the output to a new txt file

json.dump(maxValue, open("FileWithMaxSize.txt",'a+'))


### Code for output in text file and for getting virtual memory 
        
Diskusage = psutil.virtual_memory()

Dict_Diskusage = dict(Diskusage._asdict())

print (json.dumps({"DiskUsage" : Dict_Diskusage} , indent=4))

print("------------------------------------------------------------")

## Output is in csv file which will be created in the path which is given as argument

with open('DiskUsage.csv' , 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key , value in Dict_Diskusage.items():
        writer.writerow([key , value])
        
print ("Output is written to DiskUsage.csv file")
print("------------------------------------------------------------")

## Code for send an email with csv output file attached.

mail_content = "PFA Files which contains list of Files in the " + sys.argv[1] + " directory and the File with max Size"
COMMASPACE = ', '
sender_address = 'madhavibhat2@gmail.com'
sender_password = 'Feb@2019'
recipients = ["jamunakn5@gmail.com" , "madhavibhat2@gmail.com"]

message = MIMEMultipart()
message["From"] = sender_address
message["To"] = COMMASPACE.join(recipients)
message["Subject"] = "List of files with their size"

OutputFile = os.path.join(os.getcwd() , "output.csv")
DiskUsageFile = os.path.join(os.getcwd() , "DiskUsage.csv")
FileWithMaxSize = os.path.join(os.getcwd() , "FileWithMaxSize.txt")
attachments = [OutputFile , DiskUsageFile , FileWithMaxSize]

##attachments = ['C:\Users\dell-pc\Documents\Java-Xml']

for file in attachments:
    try:
        with open(file , 'rb') as fp:
            msg = MIMEBase('application' , "octet-stream")
            msg.set_payload(fp.read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
        message.attach(msg)
        
    except:
        print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
        raise
        
composed = message.as_string()

### Sending the email

try:
    with smtplib.SMTP("smtp.gmail.com" , 587) as sm:
        sm.ehlo()
        sm.starttls()
        sm.login(sender_address , sender_password)
        sm.sendmail(sender_address , recipients , composed)
        sm.close()
    print("Email has been sent with File Details!")
    print("------------------------------------------------------------")

except:
    print("Unable to send the mail. Error: " , sys.exc_info()[0])
    raise
    
            
