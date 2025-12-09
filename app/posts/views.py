from flask import render_template, redirect, url_for, flash, request
from app import db
from app.posts.models import Post, Tag
from app.users.models import User
from app.posts.forms import PostForm
from . import posts_bp


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    form.user_id.choices = [(u.id, u.username) for u in db.session.scalars(db.select(User).order_by(User.username))]
    form.tags.choices = [(t.id, t.name) for t in db.session.scalars(db.select(Tag).order_by(Tag.name))]

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.user_id.data
        )


        selected_tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
        new_post.tags.extend(selected_tags)

        db.session.add(new_post)
        db.session.commit()

        flash(f"Пост '{new_post.title}' успішно створено!", 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('create_post.html', form=form)

@posts_bp.route('/')
def get_posts():

    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()

    return render_template('posts.html', posts=posts)
@posts_bp.route('/<int:id>')
def detail_post(id):

    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form.user_id.choices = [(u.id, u.username) for u in db.session.scalars(db.select(User).order_by(User.username))]
    form.tags.choices = [(t.id, t.name) for t in db.session.scalars(db.select(Tag).order_by(Tag.name))]

    if request.method == 'GET':
        form.publish_date.data = post.posted
        form.tags.data = [t.id for t in post.tags]

    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.user_id = form.user_id.data

        post.tags.clear()
        new_tags = db.session.scalars(db.select(Tag).where(Tag.id.in_(form.tags.data))).all()
        post.tags.extend(new_tags)

        db.session.commit()
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template('create_post.html', form=form)

@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост успішно видалено!', 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template('delete_confirm.html', post=post)