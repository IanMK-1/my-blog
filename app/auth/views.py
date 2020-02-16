from . import auth
from ..models import Writer
from .auth_form import WriterRegistration, WriterLogin
from .. import db
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user


@auth.route('/signup', method=["GET", "POST"])
def signup():
    form = WriterRegistration()
    if form.validate_on_submit():
        writer = Writer(full_names=form.full_names.data, email=form.email.data,writer_password=form.writer_password.data)
        db.session.add(writer)
        db.session.commit()

        return redirect(url_for('auth.writer_login'))

    return render_template('user_auth/signup.html', signup_form=form)