from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

''' These are need to be deleted.
engine = None
Base = declarative_base()
'''

db = SQLAlchemy()