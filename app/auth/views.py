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
        writer = Writer(full_names=form.full_names.data, email=form.email.data,
                        password=form.writer_password.data)
        db.session.add(writer)
        db.session.commit()

        return redirect(url_for('auth.writer_login'))

    return render_template('writer_auth/signup.html', signup_form=form)


@auth.route('/login', methods=["GET", "POST"])
def writer_login():
    login_form = WriterLogin()
    if login_form.validate_on_submit():
        writer = Writer.query.filter_by(email=login_form.email.data).first()
        if writer is not None and writer.verify_password(login_form.writer_password.data):
            login_user(writer, login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password')

    return render_template('writer_auth/login.html', writerlogin_form=login_form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
