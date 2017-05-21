# SmartLighting
SmartLighting is VTTs project to enhance energy savings and efficiency of lighting in buildings. The system uses passive infrared sensors to turn on lights and sensors in luminaires to track times when lights are on. Every sensor works wirelessly and every event is stored in database for later inspection.

The purpose of this software is to analyze movement at the building’s monitored corridor and calculate the exact energy savings of SmartLighting system.

## Requirements
1. Python 2.7 (https://www.python.org/)
2. pip (should come paired with python)
3. PostgreSQL Database (https://www.postgresql.org/)

## Installation
Consider using virtualenv to keep your projects separate from eachother
https://virtualenv.pypa.io/en/stable/

1. make sure you have all the requirements
2. clone the repository somewhere
	> git clone https://github.com/olkorhon/SmartLightning.git
3. navigate to repository folder and install dependencies with pip
	> pip install -r requirements.txt
4. setup dbconfig.py which is found in SmartLightning/src/dbconfig.py
	> USER: your_postgres_username
	
	> PASSW: your_postgres_user_password
	
	> DBNAME: name_of_the_database_you_want_to_access
5. run main.py and optionally provide starting time for the analysis (See open issue about this)
	> python main.py 12.4.2015
