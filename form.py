from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DecimalField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class CafeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    has_toilet = BooleanField('Toilet', default=False)
    has_wifi = BooleanField('Wifi', default=False)
    has_sockets = BooleanField('Sockets', default=False)
    can_take_calls = BooleanField('Can take calls', default=False)
    coffee_price = DecimalField('Coffee', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        Length(min=6, max=30, message="Kullanıcı Adı en az 6 en fazla 30 karakter olabilir.")
    ])
    email = StringField(label="E-Posta", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        Email(message="Lütfen geçerli bir e-posta adresi girin.")
    ])
    password = PasswordField(label="Password", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        Length(min=6,max=30, message="Şifre en az 6 en fazla 30 karakter olabilir.")
    ])
    two_password = PasswordField(label="Password Confirm", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        EqualTo(fieldname='password', message="Şifreler Eşleşmiyor")
    ])
    submit = SubmitField(label="Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        Length(min=6, max=30, message="Kullanıcı Adı en az 6 en fazla 30 karakter olabilir.")
    ])
    password = PasswordField(label="Password", validators=[
        DataRequired(message="Bu alan boş bırakılamaz."),
        Length(min=6,max=30, message="Şifre en az 6 en fazla 30 karakter olabilir.")
    ])
    submit = SubmitField(label="Login")