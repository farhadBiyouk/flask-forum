from flask import Flask

from .posts.routes import blueprint as posts_bluprint
from .users.routes import blueprint as users_bluprint
from .users.models import User, Code
from . import exceptions as app_exception

from .extensions import db, migrate, login

app = Flask(__name__)


#  register blueprint
def register_bluprint(app):
	app.register_blueprint(posts_bluprint)
	app.register_blueprint(users_bluprint)


register_bluprint(app)


#  register custom errors
def register_custom_error(app):
	app.register_error_handler(404, app_exception.page_not_found)
	app.register_error_handler(500, app_exception.sever_error)


register_custom_error(app)


def register_shell_context(app):
	def shell_context():
		return {
			'db': db,
			'User': User,
			'Code': Code
		}
	
	app.register_shell_context(shell_context)


#  register config file
app.config.from_object('config.DevConfig')

#  database config
db.init_app(app)
from .users.models import User

migrate.init_app(app, db)

# authentication config

login.init_app(app)
