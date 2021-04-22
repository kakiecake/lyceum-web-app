from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    recipient_id = IntegerField("Айди получателя", validators=[DataRequired()])
    note_id = IntegerField("Айди заметки", validators=[DataRequired()])
    message_text = TextAreaField("Сообщение")
    is_anonymous = BooleanField("Анонимно")
    submit = SubmitField('Сохранить')
