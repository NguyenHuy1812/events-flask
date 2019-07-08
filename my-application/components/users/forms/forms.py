from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class SignupForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email =    StringField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit =SubmitField('Sign Up')

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