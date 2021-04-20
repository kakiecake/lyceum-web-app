import flask
from flask import jsonify, request
from models import db_session
from models.note import Note

blueprint = flask.Blueprint(
    'note_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/note', methods=['GET'])
def get_notes():
    db_sess = db_session.create_session()
    note = db_sess.query(Note).all()
    return jsonify(
        {
            'notes':
                [item.to_dict(only=('name', 'text', 'author_id', 'created_at'))
                 for item in note]
        }
    )


@blueprint.route('/api/note/<int:note_id>', methods=['GET'])
def get_one_note(note_id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    if not note:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'notes': note.to_dict(only=(
                'name', 'text', 'author_id', 'is_private', 'created_at'))
        }
    )


@blueprint.route('/api/note', methods=['POST'])
def create_note():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'text', 'author_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    note = Note(
        name=request.json['name'],
        text=request.json['text'],
        author_id=request.json['author_id'],
        is_private=request.json['is_private'],
    )
    db_sess.add(note)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    if not note:
        return jsonify({'error': 'Not found'})
    db_sess.delete(note)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/note/<int:note_id>', methods=['PUT'])
def edit_note(note_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'text', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    note = db_sess.query(Note).get(note_id)
    if not note:
        return jsonify({'error': 'Id not found'})
    note.name = request.json['name']
    note.text = request.json['text']
    note.is_private = request.json['is_private']
    db_sess.commit()
    return jsonify({'success': 'OK'})
