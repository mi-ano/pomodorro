import os
import secrets
from flask import render_template, url_for,flash, redirect, request
from app import app, db, bcrypt

from app.models import User, Post
from app.forms import Registration, Login, updateForm, createPostForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash (f'Account has been created successfully for {form.username.data} !', 'success')
        return redirect (url_for('login'))

    return render_template('registration.html', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Please check your credentials', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = updateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect (url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email



    image_file = url_for('static',filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file= image_file, form = form) 

@app.route("/new_post", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = createPostForm()
    if form.validate_on_submit():
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", "success")
        return redirect (url_for('time_for_work'))
    return render_template('time_for_work.html', form = form) 

@app.route("/review", methods = ['GET', 'POST'])
@login_required
def review():
   
    return render_template('review.html')

@app.route("/break", methods = ['GET', 'POST'])
@login_required
def contact():
   
    return render_template('breaktime.html')