from flask import Flask, request, jsonify, make_response
from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_db_name',
    'host': 'localhost',
    'port': 27017
}
app.config['SECRET_KEY'] = 'your_secret_key'
db = MongoEngine(app)

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    last_active = db.DateTimeField(default=datetime.utcnow)

def generate_token(user_id):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=30),
        'iat': datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(username=data['username'], password=hashed_password)
    new_user.save()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(username=data['username']).first()
    
    if user and check_password_hash(user.password, data['password']):
        token = generate_token(user.id)
        user.update(set__last_active=datetime.utcnow())
        return jsonify({'token': token})
    else:
        return make_response('Invalid credentials', 401)

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        print('Token is missing')
        return make_response('Token is missing', 403)
    
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        print('Bearer token malformed')
        return make_response('Bearer token malformed', 403)
    
    user_id = verify_token(token)
    
    if not user_id:
        print('Invalid or expired token')
        return make_response('Invalid or expired token', 403)
    
    user = User.objects(id=user_id).first()
    
    if not user:
        print('User not found')
        return make_response('User not found', 404)
    
    if datetime.utcnow() - user.last_active > timedelta(minutes=1):
        print('Token expired due to inactivity')
        return make_response('Token expired due to inactivity', 403)
    
    user.update(set__last_active=datetime.utcnow())
    new_token = generate_token(user.id)
    
    print('Access granted')
    return jsonify({'message': 'Access granted', 'new_token': new_token})


if __name__ == '__main__':
    app.run(debug=True)
