from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, LoginManager, UserMixin, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.fields.html5 import DateTimeLocalField
import datetime
db = SQLAlchemy()
login_manager = LoginManager()


class RatingUser(db.Model):
    __tablename__='rate'
    rater_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer)

class ProfileUser(db.Model):
    __tablename__="profile"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    avatar_url = db.Column(db.String(10000), default = 'https://pbs.twimg.com/profile_images/787106179482869760/CwwG2e2M_400x400.jpg')
    phone = db.Column(db.Integer)
    address = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
class RatingEvent(db.Model):
    __tablename__='rateevent'
    rater_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rate_event = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    rating = db.Column(db.Integer)
class Event(db.Model):
    __tablename__="events"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    eventname = db.Column(db.String(80), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    time_start =db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    image_url = db.Column(db.String(10000))
    body = db.Column(db.String(1000000))
    ticket_sold = db.relationship("Ticket",backref = "sold_ticket")
    user_rate_id = db.relationship("RatingEvent", backref = "event_rate")
    rating = db.Column(db.Integer, default = 0)
    hide = db.Column(db.String(10), default = 'no')
    stock = db.Column(db.Integer, default = 0)
    genre = db.relationship('GenreMovie', backref = 'event_genre')
    
class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    profiles = db.relationship('ProfileUser', backref= 'owner')
    events = db.relationship('Event', backref= 'owner')
    rater_id = db.relationship('RatingUser',backref ='rater', primaryjoin=(id==RatingUser.rater_id))
    target_user_id = db.relationship('RatingUser',backref = 'rated', primaryjoin=(id==RatingUser.target_user_id))
    bought_ticket = db.relationship('Ticket', backref = 'bought')
    rate_event = db.relationship('RatingEvent', backref= 'whorated')
    def __repr__(self):
        return "{}".format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Ticket(db.Model):
    __tablename__="ticket"
    id = db.Column(db.Integer, primary_key = True)
    event_id = db.Column(db.Integer , db.ForeignKey("events.id"))
    type_ticket = db.Column(db.Integer, db.ForeignKey("ticketstype.id"))
    buyer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    quantity = db.Column(db.Integer)
    totalbill = db.Column(db.Integer)
    ticket_qrcode = db.Column(db.String(1000000), unique = True)
    check_in_time = db.Column(db.Integer)
    

class Genre(db.Model):
    __tablename__="genre"
    id = db.Column(db.Integer, primary_key = True)
    genres = db.column(db.String(30))
    gen_movie = db.relationship('GenreMovie', backref = 'genre_type')

class GenreMovie(db.Model):
    __tablename__="genremovie"
    id = db.Column(db.Integer, primary_key = True)
    movie_id = db.Column(db.Integer , db.ForeignKey("events.id"))
    movie_genre = db.Column(db.Integer , db.ForeignKey("genre.id"))


class Ticket_Type(db.Model):
    __tablename__="ticketstype"
    id = db.Column(db.Integer, primary_key = True)
    price = db.Column(db.Integer)
    name = db.Column(db.String(255), nullable = False , unique = True)
    type_tic = db.relationship("Ticket", backref = "type")



