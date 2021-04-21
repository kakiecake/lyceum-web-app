import requests
from flask import Flask, render_template, redirect, make_response, jsonify, \
    request
from werkzeug.exceptions import abort
from models import db_session, note_api, message_api
from forms.register import RegisterForm
from forms.login import LoginForm
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from models.user import User
from forms.note import NoteForm
from forms.message import MessageForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    return render_template('main.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit() and form.password.data == \
            form.password_again.data:
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/notes')
def notes():
    note = requests.get('http://localhost:5000/api/note').json()
    return render_template("notes.html", notes=note['notes'])


@app.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_notes():
    form = NoteForm()
    if form.validate_on_submit():
        requests.post('http://localhost:5000/api/note',
                      json={'name': form.name.data,
                            'text': form.text.data,
                            'author_id': current_user.id,
                            'is_private': form.is_private.data}).json()
        return redirect("/notes")
    return render_template('add_notes.html', form=form,
                           title='Создание заметки')


@app.route('/notes/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_notes(id):
    form = NoteForm()
    if request.method == "GET":
        note = requests.get(f'http://localhost:5000/api/note/{id}').json()
        if note.get('error') is None:
            note = note['notes']
            form.name.data = note['name']
            form.text.data = note['text']
            form.is_private.data = note['is_private']
        else:
            abort(404)
    if form.validate_on_submit():
        requests.put(f'http://localhost:5000/api/note/{id}',
                     json={'name': form.name.data,
                           'text': form.text.data,
                           'is_private': form.is_private.data}).json()
        return redirect('/notes')
    return render_template('add_notes.html',
                           form=form,
                           title='Редактор заметки'
                           )


@app.route('/notes/del/<int:id>', methods=['GET', 'POST'])
@login_required
def del_notes(id):
    note = requests.delete(f'http://localhost:5000/api/note/{id}').json()
    if note.get('error'):
        abort(404)
    return redirect('/notes')


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    message = requests.get(
        f'http://localhost:5000/api/message/{current_user.id}').json()
    return render_template("message.html", messages1=message['messages1'],
                           messages2=message['messages2'])


@app.route('/messages/add', methods=['GET', 'POST'])
@login_required
def add_messages():
    form = MessageForm()
    if form.validate_on_submit():
        requests.post('http://localhost:5000/api/message',
                      json={'recipient_id': form.recipient_id.data,
                            'sender_id': current_user.id,
                            'note_id': form.note_id.data,
                            'message_text': form.message_text.data,
                            'is_anonymous': form.is_anonymous.data}).json()
        return redirect("/messages")
    return render_template('add_message.html', form=form,
                           title='Создание сообщения')


@app.route('/messages/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_messages(id):
    form = MessageForm()
    if request.method == "GET":
        message = requests.get(
            f'http://localhost:5000/api/one_message/{id}').json()
        if message.get('error') is None:
            message = message['message']
            form.recipient_id.data = message['recipient_id']
            form.note_id.data = message['note_id']
            form.message_text.data = message['message_text']
            form.is_anonymous.data = message['is_anonymous']
        else:
            abort(404)
    if form.validate_on_submit():
        requests.put(f'http://localhost:5000/api/message/{id}',
                     json={'recipient_id': form.recipient_id.data,
                           'note_id': form.note_id.data,
                           'message_text': form.message_text.data,
                           'is_anonymous': form.is_anonymous.data}).json()
        return redirect('/messages')
    return render_template('add_message.html',
                           form=form,
                           title='Редактор сообщения'
                           )


@app.route('/messages/del/<int:id>', methods=['GET', 'POST'])
@login_required
def del_messages(id):
    message = requests.delete(f'http://localhost:5000/api/message/{id}').json()
    if message.get('error'):
        abort(404)
    return redirect('/messages')


if __name__ == '__main__':
    db_session.global_init("db/db.sqlite")
    app.register_blueprint(note_api.blueprint)
    app.register_blueprint(message_api.blueprint)
    app.run()
