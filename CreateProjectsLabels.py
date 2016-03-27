#!/usr/bin/python

# Filename: 		CreateProjectsLabels.py
# Purpose: 			read through CSV export from OmniFocus and create the same Projects and Labels in Todoist 
# Input file: 		CSV-file export from OmniFocus in UTF-8.
# Important Note: 	OmniFocus needs to be exported in UTF-16 to keep important characters and line breaks.  To convert
#					UTF-16 to UTF-8, open the UTF-16 CSV in Sublime (for example) and "Save with Encoding" to UTF-8.
# As-is software:	No warranty here at all.  Use at your own risk and make sure all your data is backed up.
# Copyright: 		None. Released into the public domain.

# Bug report:  		Please email craig.martell@hotmail.com with "[CreateProjectsLabels Bug]" at the beginning for the subject line.
# Communication: 	Please email craig.martell@hotmail.com with "[CreateProjectsLabels Comment]" at the beginning for the subject line.

import csv
import time
from pytodoist import todoist

username = raw_input("Please enter username: ")
password = raw_input("Please enter password: ")

# Use the pytodoist library for simple task of getting all project_ids, 
# and getting all label_ids.  These were previously added using code in
# createProjectsLabels.py.  Store in a dicts for when looping through CSV file.
# A more efficient way would be to create the labels and projects as they are 
# encountered in the CSV. 

user = todoist.login(username, password)

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

		#check get_project() for None.  If so, move forward.
		if tProject and user.get_project(tProject) is None:
			print "Adding Project: " + tProject
			user.add_project(tProject)

		if tContext and user.get_label(tContext) is None:
			print "Adding Label: " + tContext
			user.add_label(tContext)

		time.sleep(2) # Helps alleviate the throttling
		
		print "Just completed row: " + str(rowCounter)
		rowCounter = rowCounter + 1
print "End"

