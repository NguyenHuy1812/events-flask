from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import DateTimeLocalField
class CreateEvent(FlaskForm):
    eventname =  StringField('Event name', validators=[DataRequired()])
    title =      StringField('Title', validators=[DataRequired()])
    time_start = DateTimeLocalField('Time to end', validators=[DataRequired()],
                              format='%Y-%m-%dT%H:%M')
    time_end = DateTimeLocalField('Time to end', validators=[DataRequired()],
                              format='%Y-%m-%dT%H:%M')
    body =  TextAreaField('Body', validators=[DataRequired()])
    image_url = StringField('Image url', validators=[DataRequired()])
    genre = SelectField(u'Choose suitable genres', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Create Event')

class EditEvent(FlaskForm):
    eventname =  StringField('Event name', validators=[DataRequired()])
    title =      StringField('Title', validators=[DataRequired()])
    time_start = DateTimeLocalField('Time to end', validators=[DataRequired()],
                              format='%Y-%m-%dT%H:%M')
    time_end = DateTimeLocalField('Time to end', validators=[DataRequired()],
                              format='%Y-%m-%dT%H:%M')
    body =  TextAreaField('Body', validators=[DataRequired()])
    image_url = StringField('Image url', validators=[DataRequired()])
    genre = SelectField(u'Choose suitable genres', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Edit Event')

class RatingFormEvent(FlaskForm):
    ratings = [(0,0), (1, 1), 
               (2, 2),  (3, 3), 
               (4, 4), (5, 5)]
    rating = SelectField(u'Rate this movie', choices=ratings,
                         validators=[DataRequired()], coerce=int)
    submit = SubmitField('Rate!!!!')
    def validate(self):
        check_validate = super(RatingFormEvent, self).validate()

        if not check_validate:
            return False

        return True