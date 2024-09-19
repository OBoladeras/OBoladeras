from gallery import get_categories
from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', gallery=get_categories())


@app.route('/gallery/<category>')
def gallery(category):    
    return render_template('gallery.html', gallery=get_categories()[category])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
