from app import app
from flask import render_template
from flask import redirect, url_for


@app.route('/')
# @app.route('/blog')
def index():
    return redirect(url_for('posts.index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404