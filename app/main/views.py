from flask import render_template,request,redirect,url_for, abort
from . import main
from ..models import User
from flask_login import login_required, current_user
from .forms import UpdateProfile
from .. import db, photos

#Views
@main.route("/")
@main.route("/home")
def index():

  '''
  View root page function that returns the index page and its data
  '''
  title = 'WORK IT!!!!'

  # Getting reviews by category
  page = request.args.get('page', 1, type=int)


  return render_template('index.html')
@main.route('/user/<uname>/update/pic', methods = ['POST'])
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname = user.username))

    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

    return render_template("profile/profile.html", user = user)

@main.route('/breaktime', methods=['GET', 'POST'])
def breaktime():
    '''
    Function the returns what the user plans to do during breaktime
    '''
    return render_template('breaktime.html')

@main.route('/worksession', methods=['GET', 'POST'])
def worksession():
    '''
    Function the returns what the user plans to do during breaktime
    '''
    return render_template('worksession.html')

@main.route('/timeforwork', methods=['GET', 'POST'])
def timeforwork():
    '''
    Function the returns what the user plans to do during time for work.
    '''
    return render_template('time_for_work.html')
