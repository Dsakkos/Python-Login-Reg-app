from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import show, user


@app.route('/')
def home():
    return render_template('new_users.html')

@app.route('/users/register', methods=['POST'])
def register_user():
    if user.User.create_user(request.form):
        return redirect('/users/dashboard')
    return redirect('/')

@app.route('/users/dashboard')
def dashboard():
    return render_template('dashboard.html', all_show = show.Show.get_all_shows(), user = user.User.get_user_by_id({"id": session['users_id']}))

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/login', methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/users/dashboard')
    return redirect('/')





