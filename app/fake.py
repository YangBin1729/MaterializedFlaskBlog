from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Tag
import random


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(body=fake.text(),
                 timestamp=fake.past_date(),
                 author=u)
        db.session.add(p)
    db.session.commit()


tags = ['python', 'flask', 'javascript', 'html', 'css', 'jquery', 'web', 'machine learning', 'algorithm', 'tutorial']

def tag_table():
    posts = Post.query.order_by(Post.timestamp.desc()).limit(30).all()
    for tag in tags:
        tagged_posts = random.sample(posts, random.randint(4,10))
        tag = Tag(name=tag,
                  posts=tagged_posts)
        db.session.add(tag)
    db.session.commit()
