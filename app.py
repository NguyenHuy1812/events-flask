import os
from flask import Flask, render_template, session, redirect, url_for, escape, request
from flask_migrate import Migrate
from datetime import datetime
from components.users import users_blueprint
from components.events import events_blueprint
from models.ticketbox import db, login_manager,User,UserMixin ,RatingUser, Event
from flask_bootstrap import Bootstrap
from flask_login import login_user, login_required, LoginManager, UserMixin, logout_user, current_user

app = Flask(__name__)
bootstrap = Bootstrap(app)
db.init_app(app)
migrate = Migrate(app, db, compare_type = False)


login_manager.init_app(app)

POSTGRES = {
    'user': 'mac',
    'pw': None,
    'db': 'ticket',
    'host': 'localhost',
    'port': 5432,
}
# POSTGRES = {
#     'user': 'sql12297586',
#     'pw': 'xsCLC9SaLP',
#     'db': 'sql12297586',
#     'host': 'sql12.freemysqlhosting.net',
#     'port': 3306,
# }

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
%(port)s/%(db)s' % POSTGRES

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql12297586:xsCLC9SaLP@sql12.freemysqlhosting.net/sql12297586'
app.config["SECRET_KEY"] = '_5#y2L"F4Q8z\n\xec]/'







#Route to index page
@app.route('/')
def something():
    event = Event.query.all()
    return render_template('index.html', name = event)
#users components
app.register_blueprint(users_blueprint, url_prefix='/users')
#Handle users/signup
#Handle users/signin
    #Oldway : 
    # @app.route('/users/signup')
    # def....

@app.route('/hello')
def hello():
    # user_1 = User.query.filter_by(username = 'huy').first()
    # print('hehehehe',user_1.username)
    # user_2 = User.query.filter_by(username = 'huy04').first()
    # print('hehehehe',user_2.username)
    # rate = RatingUser(rating = 3)
    # rate.target_user_id = user_1.id
    # user_2.rater_id.append(rate)
    # db.session.commit()
    return render_template('hello.html')

@app.route('/addevent')
def events():
    user_1 = User(username = 'huy10', name = 'huy10', email = '12312312313123123@', password = 123121313123)
    db.session.add(user_1)
    db.session.commit()
    return render_template('speaker-details.html')

#events components
app.register_blueprint(events_blueprint, url_prefix='/events')
#Handle events/create
#Handle events/delete
#Handle events/edit







if __name__ == "__main__":
    app.run(debug=True)