from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import main
from .forms import SignInForm, SettingsForm, AddPomodoroForm
from ..models import User, Settings, load_user
from .. import db


@main.route("/", methods=["GET", "POST"])
def index():
    app_name = "UNWIND"
    form = AddPomodoroForm()
    if form.validate_on_submit():
        return redirect(url_for("main.settings"))
    duration = 0
    short_break = 0
    user_settings = Settings.query.filter_by(user_id=current_user.get_id()).first()
    if user_settings:
        duration = user_settings.duration
        short_break = user_settings.short_break
    return render_template(
        "index.html",
        app_name=app_name,
        duration=duration,
        short_break=short_break,
        form=form,
    )


@main.route("/unwind")
@login_required
def unwind():
    app_name = "UNWINDING"

    return render_template("unwind.html", app_name=app_name)


@main.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        settings = Settings(
            duration=form.duration.data,
            short_break=form.short_break.data,
            date_format=form.date_format.data,
            time_format=form.time_format.data,
            user_id=current_user.get_id(),
        )
        # check the break duration is between 5 and 10 mins
        # check the duration is not more than an hour (60 mins)
        if not settings.validate_break(form.short_break.data):
            print("Break not in range 5 to 10...")
            flash("Break duration should be between 5 and 10 minutes")
        elif not settings.validate_pomodoro_time(form.duration.data):
            print("Duration not in range 0 to 60...")
            flash("Pomodoro duration should be less than 60 minutes")
        else:
            print(current_user.get_id())
            user_set = Settings.query.filter_by(user_id=current_user.get_id()).first()
            if user_set:
                # update the user settings
                print("update user settings...")
                user_set.duration = (form.duration.data,)
                user_set.short_break = (form.short_break.data,)
                user_set.date_format = (form.date_format.data,)
                user_set.time_format = form.time_format.data
                db.session.flush()
                db.session.commit()
                flash("Settings updated")
            else:
                # Save new user settings
                db.session.add(settings)
                db.session.flush()
                db.session.commit()
                flash("Settings saved")

    return render_template("settings.html", form=form)