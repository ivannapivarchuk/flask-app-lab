from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

# 🔹 Форма контактів
class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Повідомлення", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Надіслати")

# 🔹 Форма входу
class LoginForm(FlaskForm):
    username = StringField("Ім'я користувача або email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10)])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")
