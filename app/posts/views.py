from flask import render_template, redirect, url_for, flash, request
from app import db
from app.posts.models import Post
from app.posts.forms import PostForm
from . import posts_bp


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        # Створюємо пост з даних форми
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f"Пост '{new_post.title}' успішно створено!", 'success')
        return redirect(url_for('posts.create_post'))  # Пізніше замінимо на список постів

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

    # Заповнюємо форму даними з поста
    form = PostForm(obj=post)

    if request.method == 'GET':
        # Оскільки імена полів publish_date (форма) і posted (модель) різні,
        # заповнюємо дату вручну (див. методичку стор. 14)
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        # Оновлюємо поля поста даними з форми
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data

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