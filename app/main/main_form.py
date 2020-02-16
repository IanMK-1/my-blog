from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email


class UserSubscription(FlaskForm):
    username = StringField('Enter username', validators=[DataRequired()])
    email = StringField('Enter your email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


class WriterBlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    blog_post = TextAreaField('Blog', validators=[DataRequired()])
    submit = SubmitField('Add Blog Post')


class UpdateBio(FlaskForm):
    bio = TextAreaField('Your bio.', validators=[DataRequired()])
    submit = SubmitField('Submit')
