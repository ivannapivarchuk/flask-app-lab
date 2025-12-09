from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_login import current_user
from app.users.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(),
        Length(min=4, max=20),
        Regexp(r'^[A-Za-z][A-Za-z0-9_.]*$', message="Ім'я має містити лише літери, цифри, крапку або підкреслення")
    ])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Зареєструватися 🎀')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Це ім\'я вже зайняте. Будь ласка, оберіть інше.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований. Спробуйте увійти.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти ✨')


class UpdateAccountForm(FlaskForm):
    username = StringField('Ім\'я користувача', validators=[
        DataRequired(), Length(min=4, max=20)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Оновити фото профілю', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    about_me = TextAreaField('Про мене')

    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Це ім\'я вже зайняте.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Цей email вже зайнятий.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[DataRequired()])
    new_password = PasswordField('Новий пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердіть новий пароль', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Змінити пароль')