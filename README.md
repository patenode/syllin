# syllin
Syllin Readme

The syllin web app. This level is about management of the (deployment and updating)
See the syllin/ dir for syllin business logic

Directories :

	.ebextension 
		- Installs external libs on eb server
	
	.elasticbeanstalk
		- Config for deployed server environment
	
	.idea 
		- no clue

	migrations
		- This directory is actually for updating databases in place if you change the schema. Dont worry about this

	syllin 
		- contains all code for syllin project

Files
	application.py
		- This is the entry point for the web app. Run this file to run web app. This must be called application.py, with app called application, for aws-elasticbeanstalk to work.

	manage.py 
		- This is just a helper script for the database migrator. It uses the migrations library. just run it to update schema. Only think about using this if you get errors about the database schema (like unknown column error)

	requirements.txt 
		- This is for pip. This allows you to do:

			pip install requirements.txt

		to install all needed python libraries for syllin. If you install a new module, run 

			pip freeze > requirements.txt

		to update this file.
