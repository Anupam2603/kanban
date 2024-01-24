from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError
from application.models import *
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort
import datetime, pytz

#Creating parser for creating new list request
create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('title')
create_list_parser.add_argument('description')

#Creating parser for updating a list request
update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('title')

#Creating parser for creating a task request
create_task_parser = reqparse.RequestParser()
create_task_parser.add_argument('title')
create_task_parser.add_argument('content')
create_task_parser.add_argument('deadline')
create_task_parser.add_argument('complete')
create_task_parser.add_argument('list_id')

#Creating update pasrser for updating a task request.
update_task_parser = reqparse.RequestParser()
update_task_parser.add_argument('title')
update_task_parser.add_argument('content')
update_task_parser.add_argument('deadline')
update_task_parser.add_argument('complete')
update_task_parser.add_argument('list_id')


#Setting up resource fields.
resource_fields = [{'list_id': fields.Integer, 'title': fields.String, 'description': fields.String},
				   {'task_id': fields.Integer, 'title': fields.String, 'content': fields.String, 'deadline': fields.String, 'complete': fields.Integer, 'list_id': fields.Integer}]

#Creating a class for all APIs for lists.
class ListAPI(Resource):
	@marshal_with(resource_fields[0])
	def get(self, listname):
		#To retrieve the information of a list
		list = Lists.query.filter_by(title=listname).first()
		if list is None:
			raise NotFoundError(status_code=404)
		return list

	@marshal_with(resource_fields[0])
	def put(self, listname):
		# To update a list.
		list_ = Lists.query.filter_by(title=listname).first()
		if list_ is None:
			raise NotFoundError(status_code=404)
		title = update_list_parser.parse_args().get('title', None)
		if title is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_001", error_message="Title should not be none.")
		list_.title = title 
		db.session.commit()
		return list_  

	def delete(self, listname):
		# To delete a list.
		list_ = Lists.query.filter_by(title=listname).first()
		if list_ is None:
			raise NotFoundError(status_code=404)
		if list_.tasks != []:
			raise BusinessValidationError(status_code=400, error_code="Kanban_008", error_message="There are tasks belonging to this list")
		db.session.delete(list_)
		db.session.commit()
		return "", 200

	@marshal_with(resource_fields[0])
	def post(self):
		#To create a list.
		title = create_list_parser.parse_args().get('title', None)
		description = create_list_parser.parse_args().get('description', None)
		if title is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_001", error_message="Title should not be None")
		if description is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_002", error_message="Description should not be None")
		list_ = Lists.query.filter_by(title=title).first()
		if list_ is not None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_003", error_message="This list already exists")
		list_ = Lists(title=title, description=description)
		db.session.add(list_)
		db.session.commit()
		return list_


#Creating a class for all APIs for tasks.
class TaskAPI(Resource):
	@marshal_with(resource_fields[1])
	def get(self, taskname):
		#To retrieve the information of a task.
		task = Tasks.query.filter_by(title=taskname).first()
		if task is None:
			raise NotFoundError(status_code=404)
		return task

	@marshal_with(resource_fields[1])
	def put(self, taskname):
		#To update a task
		lists = Lists.query.all()
		list_ids = []
		for list_ in lists:
			list_ids.append(list_.list_id)
		
		task = Tasks.query.filter_by(title=taskname).first()
		status = task.complete
		if task is None:
			raise NotFoundError(status_code=404)
		args = update_task_parser.parse_args()
		title = args.get('title', None)
		content = args.get('content', None)
		deadline = args.get('deadline', None)
		complete = args.get('complete', None)
		list_id = args.get('list_id', None)
		if title is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_001", error_message="Title should not be none.")
		if content is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_004", error_message="Content should not be none")
		if deadline is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_005", error_message="Deadline should not be none.")
		if complete is None or int(complete) > 1 or int(complete) < 0:
			raise BusinessValidationError(status_code=400, error_code="Kanban_006", error_message="Complete should be 0 or 1")
		if list_id is None or int(list_id) not in list_ids:
			raise BusinessValidationError(status_code=400, error_code="Kanban_007", error_message="List_id should be in " + str(list_ids))
		# Calculating update date and time
		IST = pytz.timezone('Asia/Kolkata')
		curr_time = datetime.datetime.now(IST)
		date = curr_time.strftime('%Y-%m-%d')
		time = curr_time.strftime('%H:%M:%S')

		task.title, task.content = title, content
		task.deadline, task.complete = deadline, complete
		task.list_id = list_id 
		task.update_date, task.update_time = date, time

		if status == 0 and status != complete:
			task.complete_date, task.complete_time = date, time
		db.session.commit()
		return task  

	def delete(self, taskname):
		#To delete a task.
		task = Tasks.query.filter_by(title=taskname).first()
		if task is None:
			raise NotFoundError(status_code=404)
		db.session.delete(task)
		db.session.commit()
		return "", 200


	@marshal_with(resource_fields[1])
	def post(self):
		#To create a task.
		lists = Lists.query.all()
		list_ids = []
		for list_ in lists:
			list_ids.append(list_.list_id)

		args = create_task_parser.parse_args()
		title = args.get('title', None)
		
		task_exist = Tasks.query.filter_by(title=title).first()
		
		if task_exist:
			raise BusinessValidationError(status_code=400, error_code="Kanban_009", error_message="Task is already exist with this name")

		content = args.get('content', None)
		deadline = args.get('deadline', None)
		complete = args.get('complete', None)
		list_id = args.get('list_id', None)
		if title is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_001", error_message="Title should not be none.")
		if content is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_004", error_message="Content should not be none")
		if deadline is None:
			raise BusinessValidationError(status_code=400, error_code="Kanban_005", error_message="Deadline should not be none.")
		if complete is None or int(complete) != 0:
			raise BusinessValidationError(status_code=400, error_code="Kanban_006", error_message="Complete should only be 0.")
		if list_id is None or int(list_id) not in list_ids:
			raise BusinessValidationError(status_code=400, error_code="Kanban_007", error_message="List_id should be in " + str(list_ids))
		# Calculating create date and time
		IST = pytz.timezone('Asia/Kolkata')
		curr_time = datetime.datetime.now(IST)
		date = curr_time.strftime('%Y-%m-%d')
		time = curr_time.strftime('%H:%M:%S')

		task = Tasks(list_id=list_id, title=title, content=content, deadline=deadline, complete=complete, create_date=date, create_time=time)
		db.session.add(task)
		db.session.commit()
		return task

#Creating a class to get the details of lists.
class ListDetailsAPI(Resource):
	def get(self, listname):
		#To retrieve the details of particular list like: No.of completed task,
		# deadline passed tasks, and bar chart of no. of tasks vs completion date.
		import numpy as np 
		import matplotlib.pyplot as plt
		list_ = Lists.query.filter_by(title=listname).first()
		if list_ is None:
			raise NotFoundError(status_code=404)
		completed_tasks = 0
		deadline_crossed = 0
		total_tasks = 0
		completion_date = {}
		IST = pytz.timezone('Asia/Kolkata')
		curr_time = datetime.datetime.now(IST)
		date = curr_time.strftime('%Y-%m-%d')
		for task in list_.tasks:
			total_tasks += 1
			if task.complete == 1:
				completed_tasks += 1
				if task.complete_date != None:
					if task.complete_date in completion_date.keys():
						completion_date[task.complete_date] += 1
					else:
						completion_date[task.complete_date] = 1

			if task.complete == 0 and task.deadline < date:
				deadline_crossed += 1
	
		dates = list(completion_date.keys())
		no_tasks_done = list(completion_date.values())
		fig = plt.figure(figsize = (4,2))
		plt.bar(dates, no_tasks_done, color='blue', width=0.4)
		plt.xlabel("Dates")
		plt.ylabel("no_tasks_done")
		plt.title("Number of tasks done on a date")
		plt.savefig('static/images/' + listname+'.png')

		return {"Complete_Tasks": str(completed_tasks) + "/" + str(total_tasks),
				"Deadline_passed_Tasks": str(deadline_crossed) + "/" + str(total_tasks),
				"Bar Graph": "../static/images/"+listname+".png"}
	
#Creating a class to get completed tasks on a particular date.
class TaskDetailsAPI(Resource):
	def get(self, date):
		import re
		x = re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date)
		if not x:
			raise BusinessValidationError(status_code=400, error_code="Kanban_010", error_message="Please type date in 'yyyy-mm-dd' format.")
		tasks = Tasks.query.filter_by(complete_date=date).all()
		if tasks == []:
			raise NotFoundError(status_code=404)
		all_tasks_title = []
		for task in tasks:
			all_tasks_title.append(task.title)
		return {"Tasks": all_tasks_title}

