from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import ValidationError, Email, Length
from ..users.models import User, Code


class RegisterationForm(FlaskForm):
	username = StringField('username')
	email = EmailField('email', validators=[Email()])
	phone_number = StringField('phone number', validators=[Length(min=11, max=11)])
	
	def validate_phone(self, phone):
		code = Code.query.filter_by(phone_number=phone.data)
		if code:
			Code.query.filter_by(phone_number=phone.data).delete()
		
		phone = User.query.filter_by(phone_number=phone.data).first()
		if phone:
			raise ValidationError('phone number is already exists')


class CodeVerifyForm(FlaskForm):
	code = StringField('code')


class LoginForm(FlaskForm):
	phone_number = StringField('phone number ', validators=[Length(min=11, max=11)])
	
	def validate_phone(self, phone):
		code = Code.query.filter_by(phone_number=phone.data)
		if code:
			Code.query.filter_by(phone_number=phone.data).delete()
