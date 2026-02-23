from app.models import Registro
# from run import app
from datetime import datetime, timedelta
from app.models import db
from services.external_api import SendPulse

def listar_registros_no_bot():
    # instância do sendpulse
    sendpulse = SendPulse()
    registros = Registro.query.filter(Registro.esta_no_bot == True).all()
    agora = datetime.now()
    dez_minutos_atras = agora - timedelta(minutes=1)
    for i, registro in enumerate(registros):
        if registro.criado_em - timedelta(minutes=1) < dez_minutos_atras:
            try:
                sendpulse.enviar_mensagem_whatsapp(registro.telefone, 'Oi, você ainda está aí?')
                print(f'Enviado menssagem para {registro.telefone}')
                registro.quantidade_tentativas += 1
                db.session.commit()
            except Exception as e:
                print(f'Erro: {e}')
        print(f'Verificado(s) {i+1}/{len(registros)}')
    print('finalizado a verificação!')

# with app.app_context():
#     listar_registros_no_bot()
