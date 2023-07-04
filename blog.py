import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, LogInForm

app = Flask(__name__)

app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

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
        flash(f'Account {form.username.data} successfully created!', 'success')
        return redirect(url_for('home'))
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


if __name__ == '__main__':
    app.run(debug=True)
