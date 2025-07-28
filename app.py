from flask import Flask, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user
from models.usuarios import User
from models.refeicoes import Refeicao
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

# Rotas de User:
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


# Rotas de Refeições:
@app.route('/user/<int:id_user>/refeicoes', methods=["POST"])
def create_refeicoes(id_user):
    data = request.get_json()
    nome_refeicao = data.get('nome')
    data_hora = data.get('data_hora')
    dentro_dieta = data.get('dentro_dieta')
    criado_em = data.get('criado_em')
    
    user = User.query.get(id_user)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404

    try:
        data_hora = datetime.strptime(data_hora, "%d/%m/%Y - %H:%M") if data_hora else None
        criado_em = datetime.strptime(criado_em, "%d/%m/%Y") if criado_em else None
    except:
        return jsonify({'error': 'Formato de data inválido. Use DD/MM/YYYY - HH:MM para data_hora e DD/MM/YYYY para criando_em'}), 400
    
    refeicao = Refeicao(
        usuario_id=id_user,
        nome=nome_refeicao,
        data_hora=data_hora,
        dentro_dieta=dentro_dieta,
        criado_em=criado_em,
    )
    db.session.add(refeicao)
    db.session.commit()
    
    return jsonify({'message': 'Refeição adicionada com sucesso'}), 201

@app.route('/user/<int:id_user>/refeicoes', methods=["GET"])
def list_refeicoes(id_user):
    refeicoes_all = Refeicao.query.filter_by(usuario_id=id_user).all()
    refeito_list = []

    for refeicao in refeicoes_all:
        try:
            refeicao.data_hora = datetime.strftime(refeicao.data_hora, "%d/%m/%Y - %H:%M") if refeicao.data_hora else None
            refeicao.criado_em = datetime.strftime(refeicao.criado_em, "%d/%m/%Y") if refeicao.criado_em else None
        except:
            return jsonify({'Error': 'Formatação errada'}), 400

        refeito_list.append({
            'id': refeicao.id,
            'id_usuario': refeicao.usuario_id,
            'nome': refeicao.nome,
            'data_hora': refeicao.data_hora,
            'dentro_dieta': refeicao.dentro_dieta,
            'criado_em': refeicao.criado_em
        })

    return jsonify({f'Lista do ID({id_user})': refeito_list})

@app.route('/user/<int:id_user>/refeicoes', methods=["GET"])
def list_refeicoes_filter_por_data(id_user):
    data_str = request.args.get('data')  # pega ?data= da query string

    if not data_str:
        return jsonify({'message': 'Parâmetro "data" é obrigatório no formato DD/MM/YYYY'}), 400
    
    try:
        data_formatada = datetime.strptime(data_str, '%d/%m/%Y').date()
    except ValueError:
        return jsonify({'message': 'Formato de data inválido. Use DD/MM/YYYY'}), 400
    
    refeicoes_filter_por_data = Refeicao.query.filter_by(
        Refeicao.criado_em == data_formatada,
        Refeicao.usuario_id == id_user
    ).all()

    list_refeicoes_por_data = []
    for refeicao in refeicoes_filter_por_data:
        list_refeicoes_por_data.append({
            'id': refeicao.id,
            'usuario_id': refeicao.usuario_id,
            'nome': refeicao.nome,
            'data_hora': refeicao.data_hora.strftime('%d/%m/%Y - %H:%M') if refeicao.data_hora else None,
            'dentro_dieta': refeicao.dentro_dieta,
            'criado_em': refeicao.criado_em.strftime('%d/%m/%Y') if refeicao.criado_em else None
        })
    
    return jsonify({f"Refeições do usuário {id_user} em {data_str}": list_refeicoes_por_data})

@app.route('/user/<int:id_user>/refeicoes/<int:id_refeicao>', methods=['PUT'])
def atualizar_nome_refeicao(id_user, id_refeicao):
    data = request.get_json()
    
    novo_nome = data.get('novo_nome')
    if not novo_nome:
        return jsonify({'message': 'Campo "novo_nome" é obrigatório'}), 400
    
    refeicao = Refeicao.query.filter_by(id=id_refeicao, usuario_id=id_user).first()
    if not refeicao:
        return jsonify({'message': 'Refeição não encontrada'}), 404
    
    refeicao.nome = novo_nome
    db.session.commit()
    
    return jsonify({'message': 'Nome da refeição atualizado com sucesso'}), 200

@app.route('/user/<int:id_user>/refeicoes/<int:id_refeicao>', methods=['DELETE'])
def deletar_refeicao_do_user(id_user, id_refeicao):
    
    refeicao_delete = Refeicao.query.filter_by(id=id_refeicao, usuario_id=id_user).first()
    
    if not refeicao_delete:
        return jsonify({'message': 'Refeição não encontrada'}), 404
    
    db.session.delete(refeicao_delete)
    db.session.commit()
    
    return jsonify({'message': f'Refeição de ID {id_refeicao} do usuário {id_user} foi deletada'}), 200

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