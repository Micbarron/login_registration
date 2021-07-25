from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/users/register", methods=['POST'])
def register_user():
    # validate the form data
    if User.validate_registration(request.form):

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])

        }


        User.create_user(data)
    # create user if data is valid


    return redirect('/')


@app.route('/users/login', methods=['POST'])
def login_user():

    users = User.get_users_with_email(request.form)

    if len(users) != 1:
        flash("User with given email dosen't exist")
        return redirect('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password for the given user is incorrect")
        return redirect('/')

    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    session['user_last_name'] = user.last_name
    
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        flash('Please log in to view this page.')
        return redirect('/')
# redirct to a different route
    return render_template('success.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

