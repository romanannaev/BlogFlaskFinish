from flask import Blueprint
from flask import render_template
from models import Post, Tag
from flask import request
from .forms import PostForm
from app import db
from flask import redirect
from flask import url_for
#Flask security
from flask_security import login_required
#for photo
import secrets
import os
from flask import current_app
from sqlalchemy import func

posts = Blueprint('posts', __name__, template_folder='templates') # realization functionality of app posts

def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    print(hash_photo)
    _, file_extension = os.path.splitext(photo.filename)
    print(file_extension)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/img', photo_name)
    photo.save(file_path)
    print('hello')
    return photo_name

@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        if request.form['title']:
            title = request.form['title']
            body = request.form['body']
            photo = save_image(request.files.get('image'))
            try:
                post = Post(title=title, body=body, image=photo)
                db.session.add(post)
                db.session.commit()
            except:
                print('Something wrong!')
            return redirect(url_for('posts.index'))
    form = PostForm()
    return render_template('posts/create_post.html', form=form)

@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)

@posts.route('/')
def index():
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        post = Post.query.filter(func.lower(Post.title).contains(q.lower(), autoescape=True) | \
            func.lower(Post.body).contains(q.lower(), autoescape=True)) #.all() func.lower(Post.title) == func.lower(q)
    else:
        post = Post.query.order_by(Post.created.desc())  #method disc() orders lists of posts down

    pages = post.paginate(page=page, per_page=3)

    return render_template('posts/index.html', pages=pages)

@posts.route('/<slug>/')
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404() #or first()
    tags = post.tags
    return render_template('posts/post_detail.html', post=post, tags=tags)

@posts.route('/tag/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    posts = tag.posts.all() # get list and not basequery (take function all())
    return render_template('posts/tag_detail.html', tag=tag, posts=posts)

