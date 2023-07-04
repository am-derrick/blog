from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'author': 'Derrick',
        'title': 'Post 1',
        'date': '31-02-22'
    },
    {
        'author': 'Ampire',
        'title': 'Post 2',
        'date': '31-02-23'
    }
]


@app.route('/')
@app.route('/home')
def hello():
    return render_template('home.html', posts=posts)


@app.route('/about')
def new():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
