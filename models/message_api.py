import flask
from flask import jsonify, request
from models import db_session
from models.message import Message

blueprint = flask.Blueprint(
    'message_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/message/<int:id>', methods=['GET'])
def get_messages(id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).filter(Message.recipient_id == id)
    return jsonify(
        {
            'messages':
                [item.to_dict(only=('id', 'sender_id', 'note_id',
                                    'message_text', 'is_anonymous',
                                    'created_at'))
                 for item in message]
        }
    )


@blueprint.route('/api/one_message/<int:message_id>', methods=['GET'])
def get_one_message(message_id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).get(message_id)
    if not message:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'message': message.to_dict(only=('recipient_id', 'note_id',
                                             'message_text', 'is_anonymous'))
        }
    )


@blueprint.route('/api/message', methods=['POST'])
def create_message():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['recipient_id', 'sender_id', 'note_id', 'message_text',
                  'is_anonymous']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    message = Message(
        recipient_id=request.json['recipient_id'],
        sender_id=request.json['sender_id'],
        note_id=request.json['note_id'],
        message_text=request.json['message_text'],
        is_anonymous=request.json['is_anonymous'],
    )
    db_sess.add(message)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    db_sess = db_session.create_session()
    message = db_sess.query(Message).get(message_id)
    if not message:
        return jsonify({'error': 'Not found'})
    db_sess.delete(message)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/message/<int:message_id>', methods=['PUT'])
def edit_message(message_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['recipient_id', 'note_id', 'message_text', 'is_anonymous']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    message = db_sess.query(Message).get(message_id)
    if not message:
        return jsonify({'error': 'Id not found'})
    message.recipient_id = request.json['recipient_id']
    message.note_id = request.json['note_id']
    message.message_text = request.json['message_text']
    message.is_anonymous = request.json['is_anonymous']
    db_sess.commit()
    return jsonify({'success': 'OK'})
