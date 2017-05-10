from flask import render_template, request, redirect, url_for, flash
from app.model.User import User
from flask_login import login_required, login_user, logout_user, current_user
from . import auth
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        print user.verify_password(password)
        if user is not None and user.verify_password(password):
            print user.username
            login_user(user, True)
        if current_user.is_authenticated:
            print "login success"
            print url_for('main.index')
            return redirect(request.args.get('next') or url_for('main.index'))

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        print username, password, repassword
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('register.html')



@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You hava been logged out')
    return redirect(url_for('main.index'))





# test method
@auth.route('/test')
@login_required
def test():
    return "yes , you are allowed"