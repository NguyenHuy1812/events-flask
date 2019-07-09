from jinja2 import Template
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for , current_app)
from werkzeug.security import check_password_hash, generate_password_hash
from components.users.forms.forms import SignupForm, SigninForm , RatingForm ,EditProfileForm,EmailResetForm , PasswordResetForm
from models.ticketbox import User , db, login_manager  , RatingUser , Ticket, ProfileUser , Event
from flask_login import login_user, login_required, LoginManager, UserMixin, logout_user, current_user
from sqlalchemy.sql import func
from sqlalchemy import and_
from sqlalchemy import desc, asc
from itsdangerous import  URLSafeTimedSerializer
import requests


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
        return redirect(url_for('users.login'))
    return render_template('signup.html',form = form)
@users_blueprint.route('/signin',methods=('GET', 'POST'))
def login():
    form = SigninForm()
    if form.validate_on_submit():
        log_user = User.query.filter_by(
            username=form.username.data).first()
        if log_user is None:
            error = "Wrong username"
            form.username.errors.append(error)
            return render_template('signin.html', form=form)
            # flash("wrong user name")
            
        if not log_user.check_password(form.password.data):
            error = "Wrong password"
            form.password.errors.append(error)
            return render_template('signin.html', form=form)
        else:
            login_user(log_user)
            return redirect(url_for('something'))
    return render_template('signin.html',form = form)

@users_blueprint.route('/<user_id>', methods = ['POST', 'GET'])
def profile(user_id):
   
    cur_profile = ProfileUser.query.filter_by(user_id = user_id).first()
    if cur_profile is None:
        new_profile = ProfileUser(user_id = user_id)
        db.session.add(new_profile)
        db.session.commit()
    else:
        pass
    cur_user = User.query.filter_by(id = user_id).first() 
    form = RatingForm()
    rate_list1 = RatingUser.query.filter_by(target_user_id = user_id)
    cur_rate_user = RatingUser.query.filter_by(target_user_id = user_id , rater_id = current_user.id).first()
    validate_rate =  RatingUser.query.filter_by(target_user_id = user_id).first()
    result = RatingUser.query.with_entities(
             func.avg(RatingUser.rating).label("mySum")
         ).filter_by(target_user_id = user_id).first()
    if validate_rate is None:
        rate_number = 0
    elif int(user_id) == int(validate_rate.target_user_id):
        rate_number = round(result.mySum,2)
    # elif cur_rate_event is None:
    #     rate_number = float(result.mySum)
    else:
        rate_number = 0
    
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

@users_blueprint.route('/<current_user_id>/editprofile', methods = ['POST', 'GET'])
def editprofile(current_user_id):
    update_user = ProfileUser.query.filter_by(user_id = current_user_id).first()
    update_raw_user = User.query.filter_by(id = current_user_id).first()
    form = EditProfileForm(
        name = update_raw_user.name,
        email = update_raw_user.email,
        phone  = update_user.phone,
        avatar = update_user.avatar_url,
        address = update_user.address
    )
    if request.method == 'POST':
        update_user.avatar_url = form.avatar.data
        update_raw_user.name = form.name.data
        update_raw_user.email = form.email.data
        update_user.phone = form.phone.data
        update_user.address = form.address.data
        db.session.commit()
        return redirect(url_for('something')) 
    return render_template('edit-profile.html', form = form)



@users_blueprint.route('/<user_id>/ticket/<ticket_id>', methods =['POST', 'GET'])
def ticketinfor(user_id , ticket_id):
    cur_user = User.query.filter_by(id = user_id).first()
    cur_ticket = Ticket.query.filter_by(id = ticket_id).first()
    if request.method == 'POST':
        if cur_ticket.check_in_time == 0:
            return "Out of checkin"
        else:
            cur_ticket.check_in_time = Ticket.check_in_time -1
            db.session.commit()
            return redirect(url_for('users.ticketinfor',user_id = user_id,ticket_id= ticket_id, name = cur_user , ticket = cur_ticket ))
    return render_template('ticketinfor.html', name = cur_user , ticket = cur_ticket)



@users_blueprint.route('/logout')
def logout():
    logout_user()
    event = Event.query.order_by(desc(Event.time_start))
    rating = Event.query.order_by(desc(Event.rating)).slice(0,4)
    return render_template('index.html', event = event , rating = rating)

MAILGUN_API_KEY = "835247908130ab70a5901fb6c751b9dc-afab6073-9c2883e4"
MAILGUN_DOMAIN_NAME = "sandboxd30e9b056a6240d19e2b8cbacafe6718.mailgun.org"
@users_blueprint.route('/reset', methods =['POST', 'GET'])
def test_password():
    form = EmailResetForm()
    if form.validate_on_submit():
        #VALIDATE EMAIL
        try:
            user = User.query.filter_by(email = form.email.data).first_or_404()
        except:
            flash("Invalid email address" , 'error')
            return redirect(url_for("users.login"))
        #CREATE TOKEN
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = ts.dumps(form.email.data, salt='password_reset_salt')
        title = "Reset Mail"
        email = form.email.data
        password_reset_url = url_for("users.reset_with_token", token = token, _external = True)
        password_reset_url = render_template('email_password.html', password_reset_url = password_reset_url)
        #SEND TOKEN TO THE EMAIL ADDRESS
        send_mail(title, email, password_reset_url)
    return render_template('reset.html', form = form)

def send_mail(title, email, html):
    url = "https://api.mailgun.net/v3/{}/messages".format(MAILGUN_DOMAIN_NAME)
    auth = ('api', MAILGUN_API_KEY)
    data = {
        'from': f'Mailgun User <mailgun@{MAILGUN_DOMAIN_NAME}>',
        'to': email,
        'subject':title,
        'text': 'Plaintext content',
        'html': html
    }
    print('url', url)
    response = requests.post(url, auth = auth, data = data)
    response.raise_for_status()
@users_blueprint.route("/reset_token/<token>", methods =['POST', 'GET'])
def reset_with_token(token):
    try:
        ts = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = ts.loads(token, salt = 'password_reset_salt', max_age=3600)
    except:
        flash('Fail!!!!!!!!!!!!!!!!!!!!!!!!!!', 'warning')
        return redirect(url_for('users.login'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        cur_user = User.query.filter_by(email = email).first()
        cur_user.set_password(form.password.data)
        db.session.commit()  
        return redirect(url_for('users.login'))      
    return render_template('resetpass.html', form = form)