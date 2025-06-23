import mysql.connector
from flask_sqlalchemy import SQLAlchemy

from main import app

mysql.connector.connect(
    host="127.0.0.1", user="root", password="lee2836", database="TEST_DATABASE"
)

db = SQLAlchemy(app)
