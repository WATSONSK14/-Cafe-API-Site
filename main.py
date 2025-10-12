from flask import Flask
from routes.api_routes import api_bp
from routes.normal_routes import normal_bp
from flask_login import LoginManager
from model import db, User
from config import config
import os

login_manager = LoginManager()
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

app.register_blueprint(api_bp, url_prefix='/v1')
app.register_blueprint(normal_bp)

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'normal.login'
login_manager.login_message = "Giriş yapmalısınız!"
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


if '__main__' == __name__:
    app.run(debug=app.config['DEBUG'])