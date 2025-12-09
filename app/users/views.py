from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm
from . import users_bp


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
        return redirect(url_for('posts.get_posts'))  # Якщо вже увійшов - на пости

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

@users_bp.route("/account")
@login_required
def account():
    return render_template('users/account.html', title='Профіль')

@users_bp.route("/users")
@login_required
def all_users():
    users_list = db.session.scalars(db.select(User)).all()
    count = len(users_list)
    return render_template('users/users_list.html', users=users_list, count=count)