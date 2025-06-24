from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    import config
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
