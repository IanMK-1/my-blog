from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from ..models import Writer


class WriterRegistration(FlaskForm):
    full_names = StringField('Enter your full names', validators=[DataRequired()])
    email = StringField('Enter your email', validators=[DataRequired()])
    writer_password = PasswordField('Enter password', validators=[DataRequired(), EqualTo('confirm_password',
                                                                                          message='Password does not '
                                                                                                  'match')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_writer_email(self, data_field):
        if Writer.query.filter_by(email=data_field.data).first():
            raise ValidationError('There is an account with that email')


class WriterLogin(FlaskForm):
    email = StringField('Your Email Address', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

