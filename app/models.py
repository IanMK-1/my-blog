from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from . import login_manager


class Writer(db.Model, UserMixin):
    __tablename__ = 'writers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    writer_password = db.Column(db.String(255))
    comment = db.relationship('Comment', backref='comment_id', lazy='dynamic')
    blog = db.relationship('Blog', backref='blog_id', lazy='dynamic')

    # return a printable representation of the object
    def __repr__(self):
        return f'Writer{self.full_name}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.writer_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.writer_password, password)

    @login_manager.user_loader
    def load_user(writer_id):
        return Writer.query.get(int(writer_id))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)

    def save_user_details(self):
        db.session.add(self)
        db.session.commit()


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    blog_post = db.Column(db.String())
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    writer_blog = db.Column(db.Integer, db.ForeignKey('writers.id'))
    blog_comment = db.relationship('Comment', backref='blog_comment_id', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update_blog(cls, id, blog_details, title_details):
        writer_blog = Blog.query.filter_by(id=id).update({"blog_post": blog_details, "title": title_details})
        db.session.add(writer_blog)
        db.session.commit()

    @classmethod
    def obtain_all_blogs(cls):
        all_blogs = Blog.query.all()
        return all_blogs

    @classmethod
    def obtain_writer_blog(cls, id):
        writer_blog = Blog.query.filter_by(id=id).first()
        return writer_blog


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    comment = db.Column(db.String())
    writer_id = db.Column(db.Integer, db.ForeignKey('writers.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def obtain_all_comments(cls, writer_blog):
        user_comments = Comment.query.filter_by(blog_comment_id=writer_blog).all()
        return user_comments
