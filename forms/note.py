from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class NoteForm(FlaskForm):
    name = StringField("Название заметки", validators=[DataRequired()])
    text = TextAreaField("Содержание", validators=[DataRequired()])
    is_private = BooleanField("Приватная заметка")
    submit = SubmitField('Сохранить')
