# Week6/api/db.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# create SQLAlchemy + Migrate instances
db = SQLAlchemy()
migrate = Migrate()
