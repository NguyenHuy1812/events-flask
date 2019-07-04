from jinja2 import Template
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from components.users.forms.forms import SignupForm, SigninForm , RatingForm
from models.ticketbox import User , db, login_manager  , RatingUser
from flask_login import login_user, login_required, LoginManager, UserMixin, logout_user, current_user
from sqlalchemy.sql import func
from sqlalchemy import and_
#Define blueprint
users_blueprint = Blueprint('users', __name__,
                        template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@users_blueprint.route('/signup',methods=['GET', 'POST'])
def register_user():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username = form.username.data, name = form.name.data, email = form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return render_template('signup.html',form = form)
    return render_template('signup.html',form = form)
@users_blueprint.route('/signin',methods=('GET', 'POST'))
def login():
    form = SigninForm()
    if form.validate_on_submit():
        log_user = User.query.filter_by(
            username=form.username.data).first()
        if log_user is None:
            return render_template('signin.html', form=form, error='wrong username')
        if not log_user.check_password(form.password.data):
            return render_template('signin.html', form=form, error='wrong password')
        else:
            login_user(log_user)
            return redirect(url_for('something'))
    return render_template('signin.html',form = form)

@users_blueprint.route('/<user_id>', methods = ['POST', 'GET'])
def profile(user_id):
    cur_user = User.query.filter_by(id = user_id).first()
    form = RatingForm()
    rate_list1 = RatingUser.query.filter_by(target_user_id = user_id)
    cur_rate_user = RatingUser.query.filter_by(target_user_id = user_id , rater_id = current_user.id).first()
    result = RatingUser.query.with_entities(
             func.avg(RatingUser.rating).label("mySum")
         ).filter_by(target_user_id = user_id).first()
    
    if cur_rate_user is None:
        rate_number = 0
    else:
        rate_number = float(result.mySum)
    if form.validate_on_submit():
        if  cur_rate_user is not None:
            cur_rate_user.rating = form.rating.data
            db.session.commit()
            return redirect(url_for('users.profile',user_id = user_id, rate_list1 = rate_list1 ))
        else:
            new_rating = RatingUser(rater_id = current_user.id , target_user_id = user_id ,rating = form.rating.data )
            db.session.add(new_rating)
            db.session.commit()
            return redirect(url_for('users.profile',user_id = user_id ))
    return render_template('profile.html', name = cur_user , form = form , rate_number =rate_number , 
                                        cur_rate_user =cur_rate_user, rate_list1=rate_list1)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')


