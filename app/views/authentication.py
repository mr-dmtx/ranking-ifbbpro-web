from functools import wraps
from app import app
from flask import jsonify, request
import jwt
import hashlib
import sqlite3

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'msg': 'Sem autorização'}), 401
        try:
            if (check_user(request.authorization.username, request.authorization.username) is False):
                return jsonify({'msg': 'Sem autorização'}), 401
            dados = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'msg': 'Sem autorização'}), 401

        return f(*args, **kwargs)
    return decorated

def auth():
    auth = request.authorization
    if check_user(auth.username, auth.password):
        token = jwt.encode({'username': auth.username}, app.config['SECRET_KEY'])
        return jsonify({'msg': 'Validado com sucesso!', 'token': token})
    else:
        return jsonify({'msg': 'Sem autorização'}), 401


def check_user(username, password):
    print(password)
    password_hash = hashlib.md5(password.encode())
    password = password_hash.hexdigest()
    query = """
                select nome, senha
                from usuario u 
                where nome like '{}' and senha like '{}';
            """.format(username, password)
    conn = sqlite3.connect(app.config['DB_URL'])
    cursor = conn.execute(query)


    json = [{'nome': row[0], 'senha': row[1]}
            for row in cursor.fetchall()]

    conn.close()

    if(len(json) > 0):
        return True
    else:
        return False





