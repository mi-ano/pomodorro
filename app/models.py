from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError("You cannot read the password attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer())
    short_break = db.Column(db.Integer())
    date_format = db.Column(db.String(20))
    time_format = db.Column(db.String(10))
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), unique=True)

    def __repr__(self):
        return "<Settings {}>".format(self.id)

    def validate_break(self, break_time):
        if break_time >= 5 and break_time <= 10:
            return True
        return False

    def validate_pomodoro_time(self, time):
        if time >= 0 and time <= 60:
            return True
        return False

    def check_user_settings_exists(self, user_id):
        settings = Settings.query.filter_by(user_id=user_id).first()
        if settings:
            return settings.id
        return None
