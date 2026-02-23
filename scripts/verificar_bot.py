from app.models import Registro
from run import app
from datetime import datetime, timedelta
from app.models import db
import requests

def listar_registros_no_bot():
    registros = Registro.query.filter(Registro.esta_no_bot == True).all()
    agora = datetime.now()
    dez_minutos_atras = agora - timedelta(minutes=1)
    for i, registro in enumerate(registros):
        if registro.criado_em - timedelta(minutes=1) < dez_minutos_atras:
            # Desenvolver função que dispare a mensagem
            print(f'Enviado menssagem para {registro.telefone}')
            registro.quantidade_tentativas += 1
            db.session.commit()
        print(f'Verificado(s) {i+1}/{len(registros)}')
    print('finalizado a verificação!')

with app.app_context():
    listar_registros_no_bot()
