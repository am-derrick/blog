import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, LogInForm

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET_KEY'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User '{self.username}' with email '{self.email}'"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    post_date = db.Column(db.DateTime, nullable=False,
                          default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post 'Title: {self.title}' Created at: '{self.content}'"


# app context
with app.app_context():
    db.create_all()

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
