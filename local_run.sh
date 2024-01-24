#! bin/bash

echo "Executing the code for Kanban app."

if [ -d ".kanban" ]
then
	echo "Activating virtual environment"
else
	echo "No virtual environment. Please run local_setup.sh"
	exit 1
fi

#Activate the virtual environment

source .kanban/bin/activate

export ENV="development"

#Executing the code.
python main.py

