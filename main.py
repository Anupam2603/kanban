import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource, Api
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role
from flask_login import LoginManager

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful Apis
from application.api import *
api.add_resource(ListAPI, "/api/lists", "/api/lists/<string:listname>")
api.add_resource(TaskAPI, "/api/tasks", "/api/tasks/<string:taskname>")
api.add_resource(ListDetailsAPI, "/api/listdetails/<string:listname>")
api.add_resource(TaskDetailsAPI, "/api/taskdetails/<string:date>")

if __name__ == '__main__':
  # Run the Flask app
  app.debug = True
  app.run(host='0.0.0.0',port=8080)