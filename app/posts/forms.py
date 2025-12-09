from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField,SelectMultipleField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime

CATEGORIES = [
    ('news', 'Новини'),
    ('publication', 'Публікації'),
    ('tech', 'Технології'),
    ('other', 'Інше')
]


class PostForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(min=2, max=150)])
    content = TextAreaField("Текст поста", validators=[DataRequired()])
    is_active = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField('Дата публікації', format='%Y-%m-%dT%H:%M', default=datetime.utcnow)
    category = SelectField('Категорія', choices=CATEGORIES, validators=[DataRequired()])
    user_id = SelectField('Автор', coerce=int, validators=[DataRequired()])
    tags = SelectMultipleField('Теги (затисни Ctrl для вибору кількох)', coerce=int)
    submit = SubmitField("Зберегти")