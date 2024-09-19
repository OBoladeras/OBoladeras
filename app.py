from gallery import Gallery
from flask import Flask, render_template

app = Flask(__name__)
gallery = Gallery('1z90cdmzGxyai6M1uTtLmBMsfI6ymZdXJ').get_categories()

@app.route('/')
def index():

    return render_template('gallery.html', gallery=gallery)


if __name__ == '__main__':
    app.run(debug=True)
