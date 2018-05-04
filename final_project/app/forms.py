from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

# Sign-Up Form consists of 3 string fields (name, email, date) and a submit field
class SignUpForm(FlaskForm):
    name = StringField('Name (please match to table on right, if applicable)', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()], format="%m/%d/%Y")
    submit = SubmitField('Sign Up')
