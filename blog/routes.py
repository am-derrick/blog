from blog.models import User, Post
from flask import render_template, url_for, flash, redirect
from blog.forms import SignUpForm, LogInForm
from blog import app, db, bcrypt


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
    form = LogInForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error! Please check your email and password.', 'danger')
    return render_template('login.html', title='Log In', form=form)
