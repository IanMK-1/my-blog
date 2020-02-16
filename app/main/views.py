from flask import render_template, redirect, url_for, abort, request
from ..request import obtain_quote
from . import main
from .. import db, photos
from ..models import User, Writer, Blog, Comment
from .main_form import UserSubscription, WriterBlogForm, UpdateBio
from flask_login import login_required, current_user


@main.route('/')
def index():
    quote = obtain_quote()

    return render_template('index.html', quote=quote)


@main.route('/blogs')
def blogs():
    all_blogs = Blog.obtain_all_blogs()

    return render_template('blogs.html', all_blogs=all_blogs)


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


@main.route('/writer/<full_name>')
def profile(full_name):
    writer = Writer.query.filter_by(full_name=full_name).first()

    if writer is None:
        abort(404)

    return render_template("profile/profile.html", writer=writer)


@main.route('/writer/<full_name>/update_bio', methods=['GET', 'POST'])
@login_required
def update_bio(full_name):
    writer = Writer.query.filter_by(full_name=full_name).first()
    if writer is None:
        abort(404)

    form = UpdateBio()

    if form.validate_on_submit():
        writer.bio = form.bio.data

        db.session.add(writer)
        db.session.commit()

        return redirect(url_for('.profile', full_name=writer.full_name))

    return render_template('profile/update.html', form=form)


@main.route('/writer/<full_name>/update/pic', methods=['POST'])
@login_required
def update_pic(full_name):
    writer = Writer.query.filter_by(full_name=full_name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        writer.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', full_name=full_name))


@main.route('/blog_post', methods=["GET", "POST"])
@login_required
def blog_post():
    blog = WriterBlogForm()
    if blog.validate_on_submit():
        title = blog.title.data
        blog_post = blog.blog_post.data

        new_blog = Blog(title=title, blog_post=blog_post, blog=current_user)

        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('main.blogs'))

    return render_template('blog_post.html', blog=blog)


