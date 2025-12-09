import os
import secrets
from PIL import Image
from datetime import datetime
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ChangePasswordForm
from app import db, bcrypt
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from . import users_bp

@users_bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
@users_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.get_posts'))

    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'Акаунт створено для {form.username.data}! Тепер ви можете увійти.', 'success')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', title='Register', form=form)


@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.get_posts'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вітаємо, {user.username}! Ви успішно увійшли.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('posts.get_posts'))
        else:
            flash('Вхід не вдався. Перевірте email та пароль.', 'danger')

    return render_template('users/login.html', title='Login', form=form)

@users_bp.route("/logout")
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('posts.get_posts'))


@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        db.session.commit()
        flash('Ваш акаунт оновлено!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('users/account.html', title='Профіль',
                           image_file=image_file, form=form)

@users_bp.route("/users")
@login_required
def all_users():
    users_list = db.session.scalars(db.select(User)).all()
    count = len(users_list)
    return render_template('users/users_list.html', users=users_list, count=count)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@users_bp.route("/user/change-password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()

            flash('Ваш пароль успішно оновлено! 🔒', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('Невірний поточний пароль.', 'danger')

    return render_template('users/change_password.html', title='Зміна пароля', form=form)