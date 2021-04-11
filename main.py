from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'главная страница'


@app.route('/register')
def register():
    return 'регистрация'


@app.route('/login')
def login():
    return 'логин'


@app.route('/notes')
def notes():
    return 'заметки'


@app.route('/notes/<int:id>')
def note_by_id(id: int):
    return 'заметка по ID'


if __name__ == '__main__':
    app.run()
