from flask import Blueprint, render_template, request, flash, make_response, redirect



cookies = Blueprint('cookies',__name__)

@cookies.route('/setcookie', methods=['POST', 'GET'])
def setcookie(): # setter
    # print("redirect successful")
    resp = make_response(render_template('index.html'))
    resp.set_cookie('user_id', request.args['user_id'])

    return resp


@cookies.route('/getcookie')
def getcookie(): # getter
   name = request.cookies.get('user_id')
   return '<h1>welcome ' + name + '</h1>'

