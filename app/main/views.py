from flask import render_template, redirect, url_for
from ..request import obtain_quote
from . import main
from .. import db
from ..models import User, Writer, Blog, Comment
from .main_form import UserSubscription, WriterBlogForm


@main.route('/')
def index():
    quote = obtain_quote()

    return render_template('index.html', quote=quote)


@main.route('/blogs')
def blogs():
    return render_template('blogs.html')


@main.route('/subscribe', methods=["GET", "POST"])
def subscribe():
    user = UserSubscription()
    if user.validate_on_submit():
        username = user.username.data
        email = user.email.data

        new_user = User(username=username, email=email)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.blogs'))

    return render_template("subscribe.html", user=user)
