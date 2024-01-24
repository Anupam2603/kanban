# Local Setup
- Clone the project
- Run `local_setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development

# Folder Structure

- `db_directory` has the sqlite DB. It can be anywhere on the machine. Adjust the path in ``application/config.py`. 
- `application` is where our application code is
- `local_setup.sh` set up the virtualenv inside a local `.kanban` folder.
- `local_run.sh`  Used to run the flask application in development mode
- `static` - default `static` files folder. 
- `static/stylesheets/kanban.css` is stylesheet to add on some styles on the app.
- `templates` - Default flask templates folder


```
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── models.py
│   ├── api.py
│   ├── validation.py
│   └── __pycache__
│       ├── config.cpython-310.pyc
│       ├── controllers.cpython-310.pyc
│       ├── database.cpython-310.pyc
│       ├── models.cpython-310.pyc
│       ├── api.cpython-310.pyc
│       └── validation.cpython-310.pyc
├── db_directory
│   └── kanbandb.sqlite3
├── local_run.sh
├── local_setup.sh
├── main.py
├── api.yaml
├── requirements.txt
├── README.md
├── static
│   ├── download
│   ├── images    
│   ├── javascripts 
│   │   └── kanban.js
│   └── stylesheets
│       └── kanban.css
└── templates
    ├── addinglist.html
    ├── addingtask.html
    ├── confirmation.html
    ├── editlist.html
    ├── edittask.html
    ├── lists.html
    ├── nolist.html
    └── summary.html
    
```
