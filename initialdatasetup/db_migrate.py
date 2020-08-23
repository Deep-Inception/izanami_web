from backend import db
db.drop_all(bind=None)
db.create_all()
