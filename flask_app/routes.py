# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request, session, url_for, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from .utils.database.database  import database
from werkzeug.datastructures   import ImmutableMultiDict
from pprint import pprint
import json
import random
import functools
from . import socketio


db = database()

failed_attempts = {}

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)
    return secure_function

def getUser():
	return session['email'] if 'email' in session else 'Unknown'

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', default=None)
	return redirect('/')

@app.route('/processlogin', methods=["POST", "GET"])
def processlogin():
    form_fields = request.get_json()
    email = form_fields.get('email')
    password = form_fields.get('password')
    
    auth_result = db.authenticate(email, password)
    
    if auth_result.get('success'):
        session['email'] = db.reversibleEncrypt('encrypt', email)
        session['role'] = auth_result.get('role')
        # Reset failed attempts for this email
        if email in failed_attempts:
            failed_attempts[email] = 0
        return json.dumps({
            'status': 'success', 
            'role': auth_result.get('role')
        })
    else:
        # Track failed attempts by email
        failed_attempts[email] = failed_attempts.get(email, 0) + 1
        return json.dumps({
            'status': 'fail',
            'attempts': failed_attempts[email],
            'error': auth_result.get('error', 'Authentication failed')
        })

#######################################################################################
# CHATROOM RELATED
#######################################################################################
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', user=getUser())

@socketio.on('joined', namespace='/chat')
def joined(message):
    join_room('main')
    email = db.reversibleEncrypt("decrypt", getUser())
    role = session.get('role', 'guest')
    className = 'ownerMsg' if role == 'owner' else 'guestMsg'

    emit('status', {
        'msg': f"{email} has entered the room.",
        'role': className
    }, room='main')


@socketio.on('leave', namespace='/chat')
def leave():
    email = db.reversibleEncrypt("decrypt", getUser())
    role = session.get('role', 'guest')
    className = 'ownerMsg' if role == 'owner' else 'guestMsg'

    emit('status', {
        'msg': f"{email} has left the room.",
        'role': className
    }, room='main')


@socketio.on('send', namespace='/chat')
def sendMessage(message):
    email = db.reversibleEncrypt("decrypt", getUser())
    role = session.get('role', 'guest')
    className = 'ownerMsg' if role == 'owner' else 'guestMsg'

    emit('chat', {
        'msg': f"{email}: {message}",
        'role': className
    }, room='main')

#######################################################################################
# OTHER
#######################################################################################
@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	print(db.query('SELECT * FROM users'))
	x = random.choice(['I like to powerlift.','I make smoothies every morning.','I listen to a lot of music.'])
	return render_template('home.html', user=getUser(), fun_fact = x)

@app.route("/piano")
def piano():
    return render_template("piano.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/processfeedback', methods = ['GET','POST'])
def processfeedback():
	feedback = db.GetFeedbackData()
	name = request.form.get('name')
	email = request.form.get('email')
	comment = request.form.get('comment')
	db.addFeedback([name, email, comment])
	print("feedback:",feedback)
	return render_template('processfeedback.html', feedback = feedback)


@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


@app.context_processor
def inject_db():
    return {'db': db}