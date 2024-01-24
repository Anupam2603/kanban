from flask import Flask, request, redirect, url_for
from flask import render_template, send_file
from flask import current_app as app
from application.models import *
import datetime, pytz
from flask_security import login_required, roles_accepted, roles_required


@app.route("/", methods=["GET", "POST"])
@login_required
def all_list():
	#To get all the task arranged listwise on kanban board.
	lists = Lists.query.all()
	n = len(lists)
	if n == 0:
		return render_template("nolist.html")
	else:
		return render_template("lists.html", lists=lists)


@app.route("/addinglist", methods=["GET", "POST"])
@login_required
def addinglist():
	#Controller for adding a list.
	if request.method == "GET":
		return render_template("addinglist.html")
	elif request.method == "POST":
		special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
		lname = request.form.get("lname")
		list_ = Lists.query.filter_by(title=lname).first()
		if list_ != None:
			return ("List already exists with this name")
		for c in lname:
			if c in special_characters:
				return ("error")
		description = request.form.get("description")
		if len(description) > 50:
			return ("error")
		
		list_ = Lists(title=lname, description=description)
		db.session.add(list_)
		db.session.commit()
		return redirect(url_for('all_list'))


@app.route("/addingtask/<list>", methods=["GET", "POST"])
@login_required
def addingtask(list):
	#Controller for adding a task.
	if request.method == "GET":
		return render_template("addingtask.html", list=list)
	elif request.method == "POST":
		special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
		title = request.form.get("title")
		task_ = Tasks.query.filter_by(title=title).first()
		if task_ != None:
			return ("Task already exists with this name.")
		for c in title:
			if c in special_characters:
				return ("error")
		content = request.form.get("content")
		if len(content) > 50:
			return ("error")
		deadline = request.form.get("deadline")
		completion = request.form.get("completion")
		if completion == "1":
			return ("error")
		else:
			completion = 0
		listid = Lists.query.filter_by(title=list).first().list_id
		
		IST = pytz.timezone('Asia/Kolkata')
		curr_time = datetime.datetime.now(IST)
		date = curr_time.strftime('%Y-%m-%d')
		time = curr_time.strftime('%H:%M:%S')

		if deadline < date:
			return ("error")
		task = Tasks(list_id=listid, title=title, content=content, deadline=deadline, complete=completion, create_date=date, create_time=time)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('all_list'))


@app.route("/editlist/<default>", methods=["GET", "POST"])
@login_required
def editlist(default):
	#Controllers for editing a list.
	if request.method == 'GET':
		return render_template("editlist.html", default=default)
	elif request.method == 'POST':
		lname = request.form.get("lname")
		special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
		for c in lname:
			if c in special_characters:
				return("error")
		list_ = Lists.query.filter_by(title=lname).first()
		if list_!= None:
			return "list already exists"
		else:
			list_= Lists.query.filter_by(title=default).first()	
			list_.title = lname 
			db.session.add(list_)
			db.session.commit()
			return redirect(url_for('all_list'))


@app.route("/deletelist/<list>", methods=["GET"])
@login_required
def deletelist(list):
	#Controller for deleting a list.
	listid = Lists.query.filter_by(title=list).first().list_id 
	tasks = Tasks.query.filter_by(list_id = listid).all()
	if len(tasks) == 0:
		list_ = Lists.query.filter_by(title=list).first()
		db.session.delete(list_)
		db.session.commit()
		return redirect(url_for("all_list"))
	else:
		lists=Lists.query.all()
		for list_ in lists:
			if list_.title == list:
				lists.remove(list_)
		return render_template("confirmation.html", tasks=tasks, lists=lists, list=list)


@app.route("/moveall/<source>/<to>", methods=["GET"])
@login_required
def moveall(source,to): 
	#Controller for moving all the tasks to a different list.
	tasks = Lists.query.filter_by(title=source).first().tasks
	listid = Lists.query.filter_by(title=to).first().list_id 
	for task in tasks:
		task.list_id = listid 
		db.session.add(task)
	db.session.commit()
	list = Lists.query.filter_by(title=source).first()
	db.session.delete(list)
	db.session.commit()
	return redirect(url_for("all_list"))


@app.route("/deleteall/<source>", methods=["GET"])
@login_required
def deletall(source):
	#Controller for deleting all tasks of a list and delete that particular list also.
	tasks = Lists.query.filter_by(title=source).first().tasks
	for task in tasks:
		db.session.delete(task)
	db.session.commit()
	list = Lists.query.filter_by(title=source).first()
	db.session.delete(list)
	db.session.commit()
	return redirect(url_for("all_list"))


@app.route("/edittask/<list_>/<task>", methods=["GET", "POST"])
@login_required
def edittask(list_,task):
	#Controller for editing a task.
	lists = Lists.query.all()
	task = Tasks.query.filter_by(title=task).first()
	status = task.complete
	if request.method == "GET":
		return render_template("edittask.html", task=task, lists = lists, list_=list_)
	elif request.method == "POST":
		special_characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '<', '>', '~', '`']
		list = request.form.get("list")
		listid = Lists.query.filter_by(title=list).first().list_id
		title = request.form.get("title")
		task_ = Tasks.query.filter_by(title=title).first()
		if task_  != None:
			return("Task already exists with this name.")
		for c in title:
			if c in special_characters:
				return("error")

		content = request.form.get("content")
		if len(content) > 50:
			return("error")
		deadline = request.form.get("deadline")
		complete = request.form.get("complete")
		if complete == "1":
			complete = 1
		else:
			complete = 0

		IST = pytz.timezone('Asia/Kolkata')
		curr_time = datetime.datetime.now(IST)
		date = curr_time.strftime('%Y-%m-%d')
		time = curr_time.strftime('%H:%M:%S')

		task.list_id, task.title, task.content = listid, title, content
		task.deadline, task.complete = deadline, complete
		task.update_date, task.update_time = date, time

		if status == 0 and status != complete:
			task.complete_date, task.complete_time = date, time

		db.session.commit()
		return redirect(url_for("all_list"))



@app.route("/deletetask/<task>", methods=["GET"])
@login_required
def deletetask(task):
	#Controller for deleting a task.
	task = Tasks.query.filter_by(title=task).first()
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for("all_list"))


@app.route("/movetask/<task>/<to>", methods=["GET"])
@login_required
def movetask(task,to):
	# Controller for moving a task.
	task = Tasks.query.filter_by(title=task).first()
	listid = Lists.query.filter_by(title=to).first().list_id 
	task.list_id = listid 
	db.session.commit()
	return redirect(url_for("all_list"))


@app.route("/summary", methods=["GET"])
@login_required
def summary():
	#Controller for getting summary listwise.
	import numpy as np 
	import matplotlib.pyplot as plt
	lists = Lists.query.all()
	completed_tasks = {}
	deadline_crossed = {}
	total_tasks = {}
	completion_date = {}
	IST = pytz.timezone('Asia/Kolkata')
	curr_time = datetime.datetime.now(IST)
	date = curr_time.strftime('%Y-%m-%d')
	for list_ in lists:
		completed_tasks[list_.title], deadline_crossed[list_.title], total_tasks[list_.title], completion_date[list_.title] = 0, 0, 0, {}
		for task in list_.tasks:
			total_tasks[list_.title] += 1
			if task.complete == 1:
				completed_tasks[list_.title] += 1
				if task.complete_date != None:
					if task.complete_date in completion_date[list_.title].keys():
						completion_date[list_.title][task.complete_date] += 1
					else:
						completion_date[list_.title][task.complete_date] = 1

			

			if task.complete == 0 and task.deadline < date:
				deadline_crossed[list_.title] += 1
	for key in completion_date.keys():
		if completed_tasks[key] > 0:
			dates = list(completion_date[key].keys())
			no_tasks_done = list(completion_date[key].values())
			fig = plt.figure(figsize = (4,2))
			plt.bar(dates, no_tasks_done, color='blue', width=0.4)
			plt.xlabel("Dates")
			plt.ylabel("no_tasks_done")
			plt.title("Number of tasks done on a date")
			plt.savefig('static/images/' + key+'.png')
	return render_template("summary.html",lists=lists,total_tasks=total_tasks, completed_tasks=completed_tasks, deadline_crossed=deadline_crossed)

@app.route("/export", methods=["GET"])
@login_required
def export():
	#Controller for exporting the list in .csv extension.
	lists = Lists.query.all()
	f = open('static/download/list.csv', 'w')

	header = "list_id,title,description,tasks\n"
	f.write(header)
	for list_ in lists:
		row = str(list_.list_id)+","+list_.title+","+list_.description+','
		tasks = []
		for task in list_.tasks:
			row += str(task.title) + " "
		row = row + '\n'
		f.write(row)

	f.close()
	path = 'static/download/list.csv'
	return send_file(path, as_attachment=True)

