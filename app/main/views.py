from flask import render_template, redirect, url_for, abort, request
from ..request import obtain_quote
from . import main
from .. import db, photos
from ..models import User, Writer, Blog, Comment
from .main_form import UserSubscription, WriterBlogForm, UpdateBio, UserCommentForm
from flask_login import login_required, current_user
from ..email import mail_message


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
    user = User.query.all()

    if blog.validate_on_submit():
        title = blog.title.data
        blog_post = blog.blog_post.data

        new_blog = Blog(title=title, blog_post=blog_post, blog_id=current_user)

        db.session.add(new_blog)
        db.session.commit()

        mail_message("Welcome to my blog", "email/blog_notification", user.email)

        return redirect(url_for('main.blogs'))

    return render_template('blog_post.html', blog=blog)


@main.route('/comment/<int:id>', methods=["GET", "POST"])
def comment(id):
    user_form = UserCommentForm()
    writer_blog = Blog.obtain_writer_blog(id)

    if user_form.validate_on_submit():
        username = user_form.username.data
        comment = user_form.comment.data

        user_comment = Comment(username=username, comment=comment, blog_id=current_user, blog_comment_id=writer_blog)
        db.session.add(user_comment)
        db.session.commit()

        return redirect('/comment/{writer_blog_id}'.format(writer_blog_id=writer_blog.id))

    date_of_post = writer_blog.posted_at

    comments = Comment.obtain_all_comments(writer_blog)

    return render_template('comment.html', writer_blog=writer_blog, user_form=user_form, comments=comments,
                           date=date_of_post, title="Comments")


@main.route('/blog/<int:id>/update', methods=["GET", "POST"])
@login_required
def update_blog(id):
    writer = Blog.query.filter_by(id=id).first()

    if writer is None:
        abort(404)

    form = WriterBlogForm()

    if form.validate_on_submit():
        writer.title = form.title.data
        writer.blog_post = form.blog_post.data
        db.session.commit()

        return redirect(url_for('main.comment', id=writer.id))

    date_of_post = writer.posted_at
    comments = Comment.obtain_all_comments(writer)

    return render_template('comment.html', user_form=form, date=date_of_post, writer_blog=writer, comments=comments,
                           title="Update blog")


@main.route('/blog/<int:id>/delete', methods=["GET", "POST"])
@login_required
def delete_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    db.session.delete(blog)
    db.session.commit()

    return redirect(url_for('main.blogs'))


@main.route('/comment/<uname>/delete', methods=["GET", "POST"])
@login_required
def delete_comment(uname):
    user_comment = Comment.query.filter_by(username=uname).first()
    print(user_comment)
    db.session.delete(user_comment)
    db.session.commit()

    return redirect(url_for('main.blogs'))
