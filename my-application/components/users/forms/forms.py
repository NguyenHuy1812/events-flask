from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length , InputRequired
from models.ticketbox import User
class SignupForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email =    StringField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit =SubmitField('Sign Up')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has been registered!!!")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered!!!")

class SigninForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit =SubmitField('Sign In')
    

class EditProfileForm(FlaskForm):
    # username = StringField('User name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email =    StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone' )
    avatar = StringField('Avatar')
    address = StringField('Address')
    submit = SubmitField('Change')

class EmailResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Forgot Password')

class PasswordResetForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Change password')

class RatingForm(FlaskForm):
    ratings = [(0,0), (1, 1), 
               (2, 2),  (3, 3), 
               (4, 4), (5, 5)]
    rating = SelectField(u'Rate this movie', choices=ratings,
                         validators=[DataRequired()], coerce=int)
    submit = SubmitField('Rate!!!!')
    def validate(self):
        check_validate = super(RatingForm, self).validate()

        if not check_validate:
            return False

        return True