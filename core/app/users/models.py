from ..databases import BaseModel
from ..extensions import db, login

from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
	return User.query.get(user_id)


class User(BaseModel, UserMixin):
	username = db.Column(db.String(120), unique=True, nullable=True)
	email = db.Column(db.String(120), unique=True, nullable=True)
	phone_number = db.Column(db.String(11), unique=True, nullable=False)
	
	def __repr__(self):
		return f'{self.__class__.__name__}:{self.id} - {self.username}'


class Code(BaseModel):
	code = db.Column(db.Integer, nullable=False)
	phone_number = db.Column(db.String(11), unique=True, nullable=False)
	expire_time = db.Column(db.DateTime, nullable=False)
	
	def __repr__(self):
		return f'{self.__class__.__name__}:{self.id} - {self.phone_number}'
