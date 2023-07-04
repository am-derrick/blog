import os
from flask import Flask, render_template, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = str(os.environ.get(
    'SECRET_KEY'))  # ToDo try os.getenv()

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
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def new():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
