from textwrap import indent
from django.shortcuts import render
from flask import Blueprint, render_template, request, flash, make_response, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .flaskDB import Post, User, Initial_Post, Responding_Post
from . import db, cache
from sqlalchemy.sql import and_
from random import randint
from .response import get_all_replies_by_post, get_letters_chain, get_letters_chain, pull_posts_from_database, push_response, get_post_by_id, get_all_posts_by_user, reply_chain_subsequent
import json
import datetime



views = Blueprint('views', __name__)


@views.route('/read')
def pull_message(*args, **kwargs):

    posts = pull_posts_from_database(db=db, user_id=request.cookies.get('user_id'))
    print("request made!")
    if 'local' not in request.args:
        

        '''previous solution attempt: depreciated'''
        # post_index = 0
        # posts_json = {}
        # for i in range(len(posts)):
        #     posts_json[""+str(i)] = posts[i].get_JSON()
        # resp = make_response(render_template('read_letter.html', posts=posts, i=post_index))
        # print(str(posts_json))
        # resp.set_cookie('posts', json.dumps(posts_json), expires=datetime.datetime.utcnow() + datetime.timedelta(seconds=60))

        return render_template('read_letter.html', posts=posts)
    else:
        selected_post = posts[0]
        if posts[0].id == request.cookies.get('selectedId'):
            selected_post = posts[1]
        return jsonify(selected_post.get_JSON())
    #     post_index = int(request.args['index'])
    #     posts_json = json.loads(request.cookies.get('posts'))
    #     posts = []
    #     for i in range(len(posts_json)):
    #         post = Post()
    #         post.load_from_JSON(json_data=posts_json[str(i)])


@views.route('/testposts')
def test():
    return json.dumps(request.cookies.get('posts'),indent=4)



@views.route('/', methods=['GET','POST'])
def home():

    # if not request.args.get('post'):
    #     post = Post()
    # else:
    #     post = request.args['post']

    if not ('user_id' in request.cookies):
        new_user = User()
        db.session.add(new_user)
        db.session.commit()
        user_id = new_user.id
        print(f'userid={user_id}')
        # print(url_for('views.set_cookie', user_id=user_id))
        return redirect(url_for('cookies.setcookie',user_id=user_id,post=post))

    else:
        user_id = request.cookies.get('user_id')
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            new_user = User(id=user_id)
            db.session.add(new_user)
            db.session.commit()
        print(f'cookie: {user_id}')

    return render_template('index.html')


@views.route('/responses', methods=['GET','POST'])
def response_page():
    u = User.query.filter_by(id=request.cookies.get("user_id")).first()

    if u:
        return render_template('responses.html',user=u)

@views.route('/create', methods=['GET','POST'])
def new_letter_page():
    if request.method == 'GET':
        return render_template('new_letter.html')

    if request.method == 'POST': # submit button being pressed
        message = request.form.get('content')
        subject = request.form.get('title')
        if len(message) < 1:
            flash("message is too short", category="error")
        elif len(subject)<1:
            flash("please enter a subject", category="error")
        else:
            new_post = Post(content=message,subject=subject,user_id=request.cookies['user_id'])
            db.session.add(new_post)
            db.session.commit()
            
            initial_post_entry = Initial_Post(author_id=request.cookies['user_id'],post_id=new_post.id)
            db.session.add(initial_post_entry)
            db.session.commit()
            print("data added")
            # flash('Your message has been sent!', category='success')
        return redirect(url_for('views.home'))


@views.route('/list')
def letter_list_page():
    all_posts = get_all_posts_by_user(db=db, user_id=request.cookies.get('user_id'))
    letters_sent = []
    response_sent = []
    all_replies = {}
    for post in all_posts:
        if post.is_reply and len(reply_chain_subsequent(db, post.id))==1:
            response_sent.append((post, get_letters_chain(db, post.id)[0]))
        else:
            letters_sent.append(post)
            post_replies = get_all_replies_by_post(db=db, post_id=post.id)
            all_replies[post.id] = post_replies

            

    print(response_sent)
    print(letters_sent)
    return render_template('letter_list.html', posts_sent=letters_sent, replies_list=all_replies, responses_sent=response_sent)



@views.route('/respond', methods=['POST'])
def post_response():
    if request.method == 'POST':
        push_response(db=db, 
        user_id=request.cookies.get('user_id'), 
        original_post_id=request.form.get('selectedPostId'), 
        reply_content=request.form.get('responseContent'))
    return redirect(url_for('views.home'))


def set_cookies(page, user):
    resp = make_response(render_template(page))
    resp.set_cookie('user_id', user)

    return resp


@views.route('/allresponses/<int:id>', methods=['GET','POST'])
def all_responses(id):
    all_replies = get_letters_chain(db=db, reply_id=id)
    return str([r.id for r in all_replies])



