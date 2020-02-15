from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email


class UserSubscription(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired()])
    email = StringField('Enter your email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')
