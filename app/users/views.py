from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session, make_response
)
from datetime import datetime, timedelta

users_bp = Blueprint("users", __name__, template_folder="templates")

# --- Головна сторінка входу ---
@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        if username == "admin" and password == "1234":
            session["user"] = username
            msg = "запам'ятати мене" if remember else "не запам'ятовувати"
            flash(f"Вхід успішний для {username}! Опція: {msg}.", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Невірні дані для входу!", "error")
            return redirect(url_for("users.login"))
    return render_template("users/login.html", form=form)



# --- Профіль ---
@users_bp.route("/profile")
def profile():
    if "user" not in session:
        flash("Будь ласка, увійдіть у систему!", "warning")
        return redirect(url_for("users.login"))

    # Отримуємо поточні кукі з request
    cookies = request.cookies
    color = cookies.get("color_scheme", "light")
    return render_template("users/profile.html", user=session["user"], cookies=cookies, color=color)


# --- Вихід ---
@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли з системи!", "info")
    return redirect(url_for("users.login"))


# --- Додавання кукі ---
@users_bp.route("/add_cookie", methods=["POST"])
def add_cookie():
    if "user" not in session:
        flash("Увійдіть, щоб керувати кукі!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    value = request.form.get("value")
    days = int(request.form.get("days", 1))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key, value, expires=datetime.now() + timedelta(days=days))
    flash(f"Кукі '{key}' успішно додано!", "success")
    return resp


# --- Видалення кукі ---
@users_bp.route("/delete_cookie", methods=["POST"])
def delete_cookie():
    if "user" not in session:
        flash("Увійдіть, щоб керувати кукі!", "warning")
        return redirect(url_for("users.login"))

    key = request.form.get("key")
    resp = make_response(redirect(url_for("users.profile")))

    if key == "all":
        for k in request.cookies.keys():
            resp.delete_cookie(k)
        flash("Усі кукі видалено!", "info")
    else:
        resp.delete_cookie(key)
        flash(f"Кукі '{key}' видалено!", "info")
    return resp


# --- Зміна кольорової схеми ---
@users_bp.route("/set_color/<scheme>")
def set_color(scheme):
    if "user" not in session:
        flash("Спочатку увійдіть!", "warning")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("color_scheme", scheme, max_age=60*60*24*30)
    flash(f"Кольорова схема змінена на {scheme}!", "success")
    return resp
from app.forms import ContactForm, LoginForm
import logging
from flask import flash, redirect, url_for, render_template, session, request

# 🔹 Логування у файл
logging.basicConfig(filename="contact_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

@users_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        logging.info(f"Contact: {name} ({email}) - {message}")
        flash(f"Повідомлення від {name} ({email}) успішно відправлено!", "success")
        return redirect(url_for("users.contact"))  # Post/Redirect/Get
    elif request.method == "POST":
        flash("Помилка у формі! Перевірте введені дані.", "error")
    return render_template("users/contact.html", form=form)
