from flask import request, jsonify, Blueprint
from .models import Registro
from datetime import datetime
from .models import db
from dotenv import load_dotenv
import os

load_dotenv()

main = Blueprint('main', __name__)

# rotas
@main.route('/criar-registro/', methods=['POST'])
def registro_create():
    # obtendo o token do sendpulse
    token = request.args.get('token')
    if token != os.getenv('TOKEN_SENDPULSE'):
        return jsonify({'message': 'Acesso não permitido!'}), 401
    
    # obtendo os dados do sendpulse
    data = request.json
    if not data:
        return jsonify({'message': 'Nenhuma informação recebida!'})
    dados = data[0].get('contact')
    telefone = dados.get('phone')
    # verificando se o registro já existe
    registro = Registro.query.filter(Registro.telefone == telefone).first()
    criado_em = datetime.now()
    if not registro:
        novo_registro = Registro(
            telefone=telefone,
            criado_em=criado_em,
        )
        db.session.add(novo_registro)
    else:
        registro.esta_no_bot = True
        registro.criado_em = criado_em
    db.session.commit()
    print('Registro')
    return jsonify({'message': 'Dados recebidos com sucesso!'})


@main.route('/atualizar-registro/', methods=['POST'])
def registro_update():
    # verificando o token do sendpulse
    token = request.args.get('token')
    if token != os.getenv('TOKEN_SENDPULSE'):
        return jsonify({'message': 'Acesso não permitido!'}), 401
    # obtendo os dados do sendpulse
    data = request.json
    if not data:
        return jsonify({'message': 'Não obtive informações do sistema!'})
    dados = data[0].get('contact')
    telefone = dados.get('phone')
    registro = Registro.query.filter(Registro.telefone==telefone).first()
    registro.esta_no_bot = False
    registro.quantidade = 0
    db.session.commit()
    return jsonify({'message': 'Dados atualizados com sucesso!'})