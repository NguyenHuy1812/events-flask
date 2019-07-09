from flask import Blueprint, render_template,redirect,url_for,request, flash
from components.events.forms.forms import CreateEvent,EditEvent , RatingFormEvent
from models.ticketbox import User , db, Event , Ticket , Ticket_Type , RatingEvent
from components.users import current_user
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import and_
from flask_qrcode import QRcode
import random

qrcode = QRcode()
#Define blueprint
events_blueprint = Blueprint('events', __name__,
                        template_folder='templates')
@events_blueprint.route('<current_user_id>/create', methods = ['POST', 'GET'])
def create(current_user_id):
    form = CreateEvent()
    cur_user = User.query.filter_by(id = current_user_id).first()
    if form.validate_on_submit():
        new_event = Event(stock = form.stock.data , image_url = form.image_url.data, title = form.title.data, eventname = form.eventname.data, time_start = form.time_start.data,time_end = form.time_end.data, body = form.body.data,owner = cur_user)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('something'))
    return render_template('create.html',form = form)

@events_blueprint.route('events/<current_event_id>/delete', methods = ['POST', 'GET'])
def delete(current_event_id):
    if request.method == 'POST':
        delete_event = Event.query.filter_by(id = current_event_id).first()
        delete_event.hide = 'yes'
        db.session.commit()
        return redirect(url_for("something"))
    return render_template('delete.html')

@events_blueprint.route('/<current_user_id>/<current_event_id>/edit', methods = ['POST', 'GET'])
def edit(current_user_id,current_event_id):
    update_event = Event.query.filter_by(id = current_event_id).first()
    form = EditEvent(
        eventname = update_event.eventname,
        title = update_event.title,
        image_url = update_event.image_url,
        # time_start= datetime.strptime(update_event.time_start,'%Y-%m-%d%'),
        # time_end= datetime.strptime(update_event.time_end,'%Y-%m-%d%'),
        body= update_event.body,
    )
    cur_user = User.query.filter_by(id = current_user_id).first()
    if request.method == 'POST':
        update_event.image_url = form.image_url.data
        update_event.title = form.title.data
        update_event.eventname = form.eventname.data
        update_event.time_start = form.time_start.data
        update_event.time_end = form.time_end.data
        update_event.body = form.body.data
        update_event.owner = cur_user
        update_event.genre = form.genre.data
        db.session.commit()
        return redirect(url_for('something')) 

    return render_template('edit.html', form = form)


@events_blueprint.route('/<current_event_id>', methods = ['POST', 'GET'])
def show_event(current_event_id):
    
    form = RatingFormEvent()
    cur_event = Event.query.filter_by(id = current_event_id ).first()
    rate_list1 = RatingEvent.query.filter_by(rate_event = current_event_id)
    cur_rate_event = RatingEvent.query.filter_by(rate_event = current_event_id , rater_id = current_user.id).first()
    validate_rate =  RatingEvent.query.filter_by(rate_event = current_event_id).first()
    result = RatingEvent.query.with_entities(
             func.avg(RatingEvent.rating).label("mySum")
         ).filter_by(rate_event = current_event_id).first()
    count_ticket = Ticket.query.with_entities(
             func.sum(Ticket.quantity).label("myCount")
         ).filter_by(event_id = current_event_id).first()
    count_money = Ticket.query.with_entities(
             func.sum(Ticket.totalbill).label("myMoney")
         ).filter_by(event_id = current_event_id).first()
   
    if validate_rate is None:
        rate_number = 0
    elif int(current_event_id) == int(validate_rate.rate_event):
        rate_number = round(result.mySum,2)
    # elif cur_rate_event is None:
    #     rate_number = float(result.mySum)
    else:
        rate_number = 0
    cur_event.rating = rate_number
    db.session.commit()
    if form.validate_on_submit():
        if  cur_rate_event is not None:
            cur_rate_event.rating = form.rating.data
            db.session.commit()
            return redirect(url_for('events.show_event',current_event_id = current_event_id, rate_list1 = rate_list1 ))
        else:
            new_rating = RatingEvent(rater_id = current_user.id , rate_event = current_event_id ,rating = form.rating.data )
            db.session.add(new_rating)
            db.session.commit()
            return redirect(url_for('events.show_event',current_event_id = current_event_id ))
    return render_template('showevent.html', event = cur_event, form = form,rate_number =rate_number , 
                                        cur_rate_event =cur_rate_event, rate_list1=rate_list1 , count_ticket = count_ticket, count_money =count_money)

@events_blueprint.route('events/<current_event_id>/buyhere' , methods = ['POST', 'GET'])
def buy_ticket(current_event_id):
    if request.method == 'POST':
        tic_type = Ticket_Type.query.filter_by(name = request.form['ticket-type']).first()
        cur_event = Event.query.filter_by(id = current_event_id).first()
        if int(request.form['quantity']) <= int(cur_event.stock):    
            cur_ticket = Ticket(event_id = current_event_id , 
                            type_ticket = tic_type.id,
                            buyer_id = current_user.id, 
                            quantity = request.form['quantity'], 
                            totalbill = (int(tic_type.price) * int(request.form['quantity']) ),
                            ticket_qrcode = qrcode(str(current_event_id)+str(tic_type.id) + str(random.randint(1,101)) + str(current_user.id)+str(request.form['quantity'])+str(int(tic_type.price) * int(request.form['quantity']))),
                            check_in_time = request.form['quantity']
                            )
            db.session.add(cur_ticket)
            cur_event.stock = (int(cur_event.stock) - int(request.form['quantity']))
            db.session.commit()
        else:
            flash('out of stock!!!!!')
            return redirect(url_for('events.show_event',current_event_id = current_event_id ))
        return redirect(url_for('users.ticketinfor',user_id = current_user.id , ticket_id = cur_ticket.id))

