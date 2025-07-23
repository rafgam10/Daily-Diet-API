from flask import Flask, request, jsonify
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models.usuarios import User
from dotenv import load_dotenv
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

load_dotenv()
app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = os.getenv('API_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# CRUD

@app.route('/user', methods=["POST"])
def create_user():
    data = request.get_json()
    
    if data:
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        data_criacao = data.get('criando_em')
        
        try:
            data_criacao = datetime.strptime(data_criacao, "%d/%m/%Y") if data_criacao else None
        except:
            return jsonify({'error': 'Data inválida. Use o formato DD/MM/AAAA'}), 400
        
        senha_hashed = generate_password_hash(senha)
        
        user = User(nome=nome, email=email, senha=senha_hashed, criando_em=data_criacao)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': f"Usuário {user.nome} foi criando com sucesso"}), 201
        
    else:
        return jsonify({'message': "Nenhum dado JSON encontrado na requisição"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
def read_user(id_user):
    user = User.query.get(id_user)
    
    if user:
        return jsonify({"Username": user.nome})
    
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user', methods=['GET'])
def read_users():
    users = User.query.all()
    lista_usuario = []
    
    for user in users:
        lista_usuario.append({
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
            'criando_em': user.criando_em.strftime('%d/%m/%Y') if user.criando_em else None
        })
    
    return jsonify({'Usuários': lista_usuario}), 200

@app.route('/user/<int:id>', methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    
    if id != user.id:
        return jsonify({'message': 'Operação não permitida'}), 403

    if user and data.get('senha'):
        user.senha = data.get('senha')
        db.session.commit()
        return jsonify({'message': f"Usuário {id} atualizado com sucesso"}), 200
    
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    
    if id != user.id:
        return jsonify({'message': 'Operação não permitida'}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f"Usuário {id} deletado com sucesso"}), 200

    return jsonify({'message': 'Usuário não encontrado'}), 404




@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    
    if email and senha:
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return jsonify({"message": "Acesso realizada com sucesso"}), 200
    
    return jsonify({'message': 'Acesso negado'}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'})


if __name__ == "__main__":
    app.run(debug=True)