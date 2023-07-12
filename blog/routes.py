from blog.models import User, Post
from flask import render_template, url_for, flash, request, redirect
from blog.forms import SignUpForm, LogInForm, AccountUpdateForm
from blog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Derrick',
        'title': 'Post 1',
        'date': '31-02-22',
        'content': 'The autobiography of the Greatest man tha ever lived.'
    },
    {
        'author': 'Ampire',
        'title': 'Post 2',
        'date': '31-02-23',
        'content': 'Serving with passion, eyes glued on a mission.'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        # hash password
        hashed_pwd = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        # create user from form inputs
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_pwd)
        # add and commit to database
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account successfully created!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        # query db if user exists and compare hashed password with input password
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Error! Please check your email and password.', 'danger')
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        # update account details
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account succesfully updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # pre-poulate form with existing data
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='images/' + current_user.img_file)
    return render_template('account.html', title='Account', img_file=img_file, form=form)
