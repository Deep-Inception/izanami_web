from backend import db
from backend.domains.user import User

user = User(name='test', email='test@test.com', password='izanami')

db.session.add(user)
db.session.commit()