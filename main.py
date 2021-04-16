from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/notes')
def notes():
    return render_template('notes.html', notes=[{"title": "Название", "text": "обязательно нужно это сделать " * 3}])


@app.route('/notes/<int:id>')
def note_by_id(id: int):
    return 'заметка по ID'


@app.route('/styles.css')
def styles():
    return app.send_static_file('styles.css')


if __name__ == '__main__':
    app.run()
