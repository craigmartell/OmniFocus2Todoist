#!/usr/bin/python

# Filename: 		OmniFocus2Todoist.py
# Purpose: 			Read through CSV export from OmniFocus and create the same tasks and notes in Todoist.
# Input file: 		CSV-file export from OmniFocus in UTF-8.
# Important Note: 	OmniFocus needs to be exported in UTF-16 to keep important characters and line breaks.  To convert
#					UTF-16 to UTF-8, open the UTF-16 CSV in Sublime (for example) and "Save with Encoding" to UTF-8.
# Preprocessing:  	Assumes that all the needed Projects and Labels have already been created in Todoist.  
#					CreateProjectsLabels.py is one way to do this.  Or you can do it by hand.
# As-is software:	No warranty here at all.  Use at your own risk and make sure all your data is backed up.
#					If you make a mistake you can use deleteAllTasks.py to erase all the tasks in todoist.
# Copyright: 		None. Released into the public domain.

# Bug report:  		Please email craig.martell@hotmail.com with "[OmniFocus2Todoist Bug]" at the beginning for the subject line.
# Communication: 	Please email craig.martell@hotmail.com with "[OmniFocus2Todoist Comment]" at the beginning for the subject line.


import csv
import time
from pytodoist import todoist
from pytodoist.api import TodoistAPI

# Use the pytodoist library for simple task of getting all project_ids, 
# and getting all label_ids.  These were previously added using code in
# createProjectsLabels.py.  Store in a dicts for when looping through CSV file.
# A more efficient way would be to create the labels and projects as they are 
# encountered in the CSV. 

username = raw_input("Please enter username: ")
password = raw_input("Please enter password: ")

user = todoist.login(username, password)

projects = user.get_projects()
projectDict = {}
for project in projects:
 	projectDict[project.name] = project.id

labels = user.get_labels()
labelDict = {}
for label in labels:
	labelDict[label.name] = label.id



# Use the pytodoist.api library to add new tasks, getting the project_id and 
# label_id from the dicts created above.

api = TodoistAPI()
response = api.login('craig.martell@gmail.com', 'j84#EYz76IJA')
user_info = response.json()
user_api_token = user_info['token']

file="./OmniFocus.csv"

# Since transactions with the todoist API are throttled, you will reach
# a limit before completing the list.  Change rowStart to one more than the
# last one completed -- tracked by 'print "Just Completed row: "' below.
rowCounter = 0
rowStart = 0

taskreader = csv.reader(open(file), delimiter=',')
for row in taskreader:
	if rowCounter < rowStart:
		rowCounter = rowCounter + 1
		continue
	taskID, tType, tName, tStatus, tProject, tContext, tStartDate, tDueDate, tCompletionDate, tDuration,tFlagged,tNote = row
	tContext = str(tContext).replace(" ", "_") # Todoist doesn't allow spaces in label names.
	if tType == "Action":
		projectID = projectDict[tProject]
		labelID = "" 	# Needed to have an initialized variable when tContext is empty. 
						# OmniFocus Contexts become Todoist Labels.
		if tContext:
			labelID = labelDict[tContext]
		response = api.add_item(user_api_token, tName, **{'project_id': projectID, 'labels': '['+ str(labelID) +']', 'note': tNote})
		time.sleep(2) # Helps alleviate the throttling
		print "Just completed row: " + str(rowCounter)
		rowCounter = rowCounter + 1
print "End"

