#!/usr/bin/python

# Filename: 		deleteAllTasks.py
# Purpose: 			Delete all tasks from all projects in Todoist.  Does not delete Projects.
# As-is software:	No warranty here at all.  Use at your own risk and make sure all your data is backed up.
# Copyright: 		None. Released into the public domain.

# Bug report:  		Please email craig.martell@hotmail.com with "[DeleteAllTasks Bug]" at the beginning for the subject line.
# Communication: 	Please email craig.martell@hotmail.com with "[DeleteAllTasks Comment]" at the beginning for the subject line.

import time

from pytodoist import todoist

username = raw_input("Please enter username: ")
password = raw_input("Please enter password: ")

user = todoist.login(username, password)
projects = user.get_projects()
for project in projects:
	tasks = project.get_tasks()
	for task in tasks:
		print "Deleteing " + project.name + " : " + task.content
		task.delete()
		time.sleep(2)
print "End"
