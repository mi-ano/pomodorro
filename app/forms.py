from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()] )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('ConfirmPassword', validators=[DataRequired(),EqualTo('password') ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('The username is taken, choose another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('You already have an account')

class Login(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()] )
    remember = BooleanField('Remember me')
    password = PasswordField('Password', validators=[DataRequired()])
  
    submit = SubmitField('Log In')

class updateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()] )
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg','png'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('The username is taken, choose another')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('You already have an account')

class createPostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')