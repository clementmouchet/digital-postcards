#!flask/bin/python
import uuid
from threading import Thread
from flask import Flask, jsonify, request, make_response, url_for, render_template, current_app
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.mongoengine import MongoEngine
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail, Message
from flask.ext.babel import Babel
from flask.ext.cors import CORS
from datetime import datetime


app = Flask(__name__, static_url_path="")
app.config.from_pyfile('config.py', silent=True)
auth = HTTPBasicAuth()
db = MongoEngine(app)
bootstrap = Bootstrap(app)
babel = Babel(app)
cors = CORS(app)
mail = Mail(app)

db.init_app(app)

'''
   Postcard data model
'''


class Postcard(db.Document):
    postcard_id = db.UUIDField(default=uuid.uuid4(), binary=False, required=True)
    sent = db.BooleanField(default=False)
    views = db.IntField(default=0, min_value=0, max_value=999)
    sender = db.EmailField(max_length=255, required=True)
    sender_name = db.StringField(max_length=255, required=True)
    recipient = db.EmailField(max_length=255, required=True)
    recipient_name = db.StringField(max_length=255, required=True)
    subject = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    title = db.StringField(max_length=255, required=True)
    short_desc = db.StringField(max_length=255, required=True)
    long_desc = db.StringField(max_length=255, required=True)
    image = db.URLField(required=True)
    image_attribution = db.StringField(max_length=255, required=True)
    address_line_1 = db.StringField(max_length=255)
    address_line_2 = db.StringField(max_length=255)
    address_postcode = db.StringField(max_length=255)
    address_city = db.StringField(max_length=255)
    source_url = db.URLField(required=True)
    date_added = db.DateTimeField()
    date_sent = db.DateTimeField()
    date_modified = db.DateTimeField(default=datetime.now, required=True)
    token = db.UUIDField(default=uuid.uuid4(), binary=False, required=True)

    def get_absolute_url(self):
        url = url_for('show_postcard', postcard_id=self.postcard_id, _external=True, _scheme='https')
        return "%s?token=%s" % (url, self.token)

    def get_id(self):
        return self.postcard_id

    def get_token(self):
        return self.token

    def __unicode__(self):
        return self.postcard_id

    meta = {
        'allow_inheritance': True,
        'indexes': ['-id', 'image'],
        'ordering': ['-date_added']
    }


# Handlers

@auth.get_password
def get_password(username):
    if username == app.config['ADMIN_USER']:
        return app.config['ADMIN_PASSWORD']
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'success': False, 'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'success': False, 'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'success': False, 'error': 'Not found'}), 404)


def make_public_postcard(postcard, count_view=True):
    result = {}
    for key in ['postcard_id', 'sender', 'sender_name', 'recipient', 'recipient_name',
                'token', 'sent', 'date_sent', 'date_added', 'date_modified',
                'address_line_1', 'address_line_2', 'address_city',
                'address_postcode', 'subject', 'body', 'title', 'short_desc',
                'long_desc', 'image', 'image_attribution', 'views', 'source_url']:
        result[key] = postcard[key]
    result['url'] = postcard.get_absolute_url()

    if count_view:
        postcard.update(set__views=postcard['views'] + 1)

    return result


def send_async_email(app, msg):
    """ Send an email in a separate thread

    :param app:
    :param msg:
    """
    with app.app_context():

        return mail.send(msg)


def send_email(postcard):
    """ Build a postcard email and call send_async_email() to send it in a separate thread

    :param postcard:
    """
    msg = Message(subject=postcard.subject,
                  recipients=[postcard.recipient],
                  cc=[postcard.sender],
                  reply_to=postcard.sender,
                  body=render_template('email.txt', postcard=postcard),
                  html=render_template('email.html', postcard=postcard))
    thr = Thread(target=send_async_email, args=[app, msg])
    return thr.start()


# HTML routes

@app.route('/')
@app.route('/api/')
@app.route('/api/1/')
def index():
    return jsonify({'help': 'Get help at %s' % url_for('help', _external=True, _scheme='https')})


@app.route('/about')
def about():
    data_dict = {'heading': 'About Digital Postcards'}
    return render_template('about.html',
                           title='About',
                           data_dict=data_dict)


@app.route('/contact')
def contact():
    data_dict = {'heading': 'Digital Postcard'}
    return render_template('contact.html',
                           title='Contacts',
                           data_dict=data_dict)


@app.route('/help')
def help():
    data_dict = {'heading': 'Welcome to the Digital Postcard API documentation'}
    return render_template('help.html',
                           title='Help',
                           data_dict=data_dict)


@app.route('/postcard')
def write_postcard():
    data_dict = {'heading': 'Welcome to the Digital Postcard API documentation'}
    return render_template('postcard_input.html',
                           title='Write Postcard',
                           data_dict=data_dict)


'''
   Renders postcard from the collection
'''


@app.route('/postcard/<string:postcard_id>', methods=['GET'])
def show_postcard(postcard_id):
    token = request.args.get('token', None)
    postcard = Postcard.objects.get_or_404(postcard_id=postcard_id)
    data_dict = make_public_postcard(postcard)

    if str(token) != str(postcard['token']):
        data_dict.pop('sender', None)
        data_dict.pop('recipient', None)
        data_dict.pop('address_line_1', None)
        data_dict.pop('address_line_2', None)
        data_dict.pop('address_city', None)
        data_dict.pop('address_postcode', None)

    return render_template('postcard.html',
                           title=postcard.subject,
                           postcard=data_dict)

## Public API routes
'''
   Returns JSON postcard from the collection
'''


@app.route('/api/1/postcard/<string:postcard_id>', methods=['GET'])
def get_postcard(postcard_id):
    token = request.args.get('token', None)
    postcard = Postcard.objects.get_or_404(postcard_id=postcard_id)
    data_dict = make_public_postcard(postcard)

    if str(token) != str(postcard['token']):
        data_dict.pop('sender', None)
        data_dict.pop('recipient', None)
        data_dict.pop('address_line_1', None)
        data_dict.pop('address_line_2', None)
        data_dict.pop('address_city', None)
        data_dict.pop('address_postcode', None)
        data_dict.pop('token', None)
        data_dict.pop('url', None)

    return jsonify({'success': True, 'postcard': data_dict})


'''
    Inserts new postcard in the collection
'''


@app.route('/api/1/postcard', methods=['POST'])
def create_postcard():
    data_dict = request.get_json(force=True)
    postcard = Postcard(postcard_id=uuid.uuid4(),
                        date_added=datetime.now(),
                        sender=data_dict.get('sender'),
                        sender_name=data_dict.get('sender_name'),
                        recipient=data_dict.get('recipient'),
                        recipient_name=data_dict.get('recipient_name'),
                        subject=data_dict.get('subject'),
                        body=data_dict.get('body'),
                        title=data_dict.get('title'),
                        short_desc=data_dict.get('short_desc'),
                        long_desc=data_dict.get('long_desc'),
                        image=data_dict.get('image'),
                        image_attribution=data_dict.get('image_attribution'),
                        address_line_1=data_dict.get('address_line_1'),
                        address_line_2=data_dict.get('address_line_2'),
                        address_postcode=data_dict.get('address_postcode'),
                        address_city=data_dict.get('address_city'),
                        source_url=data_dict.get('source_url'),
                        token=uuid.uuid4())

    try:
        object = postcard.save()
    except db.ValidationError, e:
        return jsonify({'success': False, 'error': e.message, 'errors': list(e.errors)}), 400

    if app.config['SEND_MAIL'] == True:
        postcard.url = postcard.get_absolute_url()
        send_email(postcard)
        postcard.update(set__sent=True)
        postcard.update(set__date_sent=datetime.now())

    return jsonify({'success': True,
                    'postcard': make_public_postcard(object)}), 200


'''
   Sends an email about the postcard
'''


@app.route('/api/1/postcard/<string:postcard_id>', methods=['PUT'])
@auth.login_required
def update_postcard(postcard_id):
    postcard = Postcard.objects.get_or_404(postcard_id=postcard_id)
    postcard.url = postcard.get_absolute_url()
    sent_date = datetime.now()
    send_email(postcard)
    postcard.update(set__sent=True)
    postcard.update(set__date_sent=datetime.now())
    postcard.update(set__date_modified=sent_date)

    return jsonify({'success': True, 'sent': True, 'sent_date': sent_date})

# Management API routes

'''
    Lists all postcards in the collection
'''


@app.route('/api/1/postcards', methods=['GET'])
@auth.login_required
def get_postcards():
    postcards = Postcard.objects.all()
    results = []
    for postcard in postcards:
        results.append(make_public_postcard(postcard, False))

    return jsonify({'success': True, 'postcards': results})


'''
    Deletes all postcards from the collection
'''


@app.route('/api/1/postcards', methods=['DELETE'])
@auth.login_required
def delete_postcards():
    Postcard.objects.delete()
    return jsonify({'success': True})


'''
    Deletes a postcard from the collection
'''


@app.route('/api/1/postcard/<string:postcard_id>', methods=['DELETE'])
@auth.login_required
def delete_postcard(postcard_id):
    postcard = Postcard.objects.get_or_404(postcard_id=postcard_id)
    postcard.delete()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'],
            host='0.0.0.0')
