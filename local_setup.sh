#! bin/bash

echo "Creating the virtual enviroment and installing all dependencies."

#Creating virtual environmnet.
if [ -d ".kanban" ]
then
	echo ".kanban library exists.Activating virtual environment and intalling dependencies using pip"
else
	echo "Creating .kanban directory"
	python3 -m venv .kanban
fi 

# Activate virtual environment
source .kanban/bin/activate

# upgrade the pip
pip install --upgrade pip

# Installing dependencies
pip install -r requirements.txt
