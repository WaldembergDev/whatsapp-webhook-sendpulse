from flask import request, jsonify, Blueprint
from .models import Registro
from datetime import datetime
from .models import db


main = Blueprint('main', __name__)

# rotas
@main.route('/criar-registro/', methods=['POST'])
def registro_create():
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
        registro.criado_em = criado_em
    db.session.commit()
    print('Registro')
    return jsonify({'message': 'Dados recebidos com sucesso!'})


@main.route('/atualizar-registro/', methods=['POST'])
def registro_update():
    data = request.json
    if not data:
        return jsonify({'message': 'Não obtive informações do sistema!'})
    dados = data[0].get('contact')
    telefone = dados.get('phone')
    registro = Registro.query.filter(Registro.telefone==telefone).first()
    registro.esta_no_bot = False
    db.session.commit()
    return jsonify({'message': 'Dados atualizados com sucesso!'})