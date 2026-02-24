from app.models import Registro
from app import create_app
from datetime import datetime, timedelta
from app.models import db
from services.external_api import SendPulse

LISTA_MENSAGENS = ['Ainda por aí? Só passando para saber se podemos continuar.',
                   'Olá! Gostaria de saber se ainda tem interesse em prosseguir com o atendimento.',
                   'Conversa finalizada. Se precisar de algo novo, estarei por aqui!']

def listar_registros_no_bot():
    with create_app().app_context():
        # instância do sendpulse
        sendpulse = SendPulse()
        registros = Registro.query.filter(Registro.esta_no_bot == True).all()
        agora = datetime.now()
        dez_minutos_atras = agora - timedelta(minutes=10)
        for i, registro in enumerate(registros):
            if registro.quantidade_tentativas >= 2:
                registro.delete()
                contact_id = sendpulse.obter_contact_id(registro.telefone)
                sendpulse.acionar_fluxo(registro.telefone, contact_id)
                print(f'Enviado menssagem para {registro.telefone}')
                continue
            if registro.criado_em < dez_minutos_atras and (agora.hour > 7 and agora.hour < 19):
                try:
                    sendpulse.enviar_mensagem_whatsapp(registro.telefone, LISTA_MENSAGENS[1])
                    print(f'Enviado menssagem para {registro.telefone}')
                    registro.quantidade_tentativas += 1
                    db.session.commit()
                except Exception as e:
                    print(f'Erro: {e}')
            print(f'Verificado(s) {i+1}/{len(registros)}')
        print('finalizado a verificação!')
