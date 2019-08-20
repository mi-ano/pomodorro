from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(),EqualTo() ])
    submit = SubmitField(Sign Up)

class Login(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()] )
    remember = BooleanField('Remember me')
    password = PasswordField('Password', validators=[DataRequired()])
  
    submit = SubmitField(Log In)