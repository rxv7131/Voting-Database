You will need to run pip from the command line to install the requirements to run the website:
	pip install flask
	pip install flask-mysqldb
If the installation has an error, install a 64-bit version of Python if you're not already using it, 
or follow these instructions to install the C++ build tools:
	https://www.scivision.dev/python-windows-visual-c-14-required/

Make sure to change the MySQL login information in voting_database_api.py to whatever it is on your device.

To run, go into the votingdatabase folder and run from the command line: python voting_database_api.py runserver.
Go to localhost:5000.