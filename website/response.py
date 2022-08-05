'''
this file contains the back end of pulling a post from database
'''

from datetime import datetime
import random
from .flaskDB import Post, User, Initial_Post, Responding_Post
from .flaskDB import db
import datetime



def pull_posts_from_database(db, user_id):
    success = False
    tries = 0

    list_of_init_posts = []

    for i in range(8):
        id = random.randint(0, Post.query.count())
        post = Initial_Post.query.filter(Initial_Post.post_id==id, Initial_Post.author_id!=user_id).first()
        if not post:
            attempt = 1
            while not post and attempt < 10:
                id = random.randint(0, Initial_Post.query.count())
                post = Initial_Post.query.filter(Initial_Post.post_id==id, Initial_Post.author_id!=user_id).first()
                attempt += 1
            if not post:
                continue
        list_of_init_posts.append(post)
        
    if len(list_of_init_posts) != 0:
        list_of_init_posts = [*set(list_of_init_posts)]
        list_of_init_posts.sort(key=sort_post_by_date_and_pulled)

    out = [get_post_by_id(db, init_post.post_id) for init_post in list_of_init_posts]
    for i in out:
        if not i:
            out.remove(i)
    return out

def get_post_by_id(db, id):
    post = Post.query.filter_by(id=id).first()
    return post

def get_all_posts_by_user(db, user_id):
    return Post.query.filter_by(user_id=user_id).all()

def get_all_replies_by_post(db, post_id):
    responses = Responding_Post.query.filter_by(respond_to=post_id).all()
    out = []
    for r in responses:
        out.append(Post.query.filter_by(id=r.post_id).first())
    return out

def get_letters_chain(db, reply_id):
    if not Responding_Post.query.filter_by(post_id=reply_id).first():
        if Initial_Post.query.filter_by(post_id=reply_id).first():
            return [Post.query.filter_by(id=reply_id).first()]
        return [Post.query.filter_by(id=reply_id).first()]
    return reply_chain_prev(db, reply_id) + reply_chain_subsequent(db, reply_id)[1:]


def reply_chain_prev(db, post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post.is_reply:
        posts_chain = []
        posts_chain.append(post)
        return posts_chain
    else:
        respond_to_id = Responding_Post.query.filter_by(post_id=post_id).first().respond_to
        posts_chain = reply_chain_prev(db, respond_to_id)
        posts_chain.append(post)
        return posts_chain

def reply_chain_subsequent(db, post_id):
    curr_node = Responding_Post.query.filter_by(post_id=post_id).first()
    curr_letter = Post.query.filter_by(id=post_id).first()
    if curr_node.reply != None:
        posts_chain = reply_chain_subsequent(db, curr_node.reply)
        posts_chain.insert(0,curr_letter)
        return posts_chain
    else:
        posts_chain = []
        posts_chain.append(curr_letter)
        return posts_chain


def create_new_post(db, user_id, content, subject):
    new_post = Post(content=content,subject=subject,user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    
    initial_post_entry = Initial_Post(author_id=user_id,post_id=new_post.id)
    db.session.add(initial_post_entry)
    db.session.commit()



def push_response(db, original_post_id, user_id, reply_content,is_initial):
    
    resp_post_data = Post(user_id=user_id, date_posted=datetime.datetime.utcnow(), content=reply_content, is_reply=True, subject="")
    db.session.add(resp_post_data)
    db.session.commit()

    resp = Responding_Post(respond_to=original_post_id, post_id=resp_post_data.id)
    db.session.add(resp)
    db.session.commit()

    if is_initial:
        init_post = Initial_Post.query.filter_by(post_id=original_post_id).first()
        init_post.is_pulled_once = True
    else:
        original_responding_entry = Responding_Post.query.filter_by(post_id=original_post_id).first()
        original_responding_entry.reply = resp_post_data.id
    db.session.commit()


def sort_post_by_date_and_pulled(init_post):
    actual_post = Post.query.filter_by(id=init_post.post_id).first()
    time_diff = datetime.datetime.utcnow() - actual_post.date_posted
    numeric_time_diff = time_diff.total_seconds() / 60
    return numeric_time_diff if init_post.is_pulled_once else 1-(1/numeric_time_diff)

def validate_user(db, user_id, post_id):
    author_id = Post.query.filter_by(id=post_id).first().user_id
    return author_id == user_id
    