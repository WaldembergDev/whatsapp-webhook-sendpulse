from app.models import Registro
from app import create_app
from datetime import datetime, timedelta
from app.models import db
from services.external_api import SendPulse

LISTA_MENSAGENS = ['Ainda por aí? Só passando para saber se podemos continuar.',
                   'Olá! Gostaria de saber se ainda tem interesse em prosseguir com o atendimento.',
                   'Conversa finalizada. Se precisar de algo novo, estarei por aqui!']

ID_FLUXO = '68f7e4ec6b69d546bd0e734a'

def listar_registros_no_bot():
    with create_app().app_context():
        # instância do sendpulse
        sendpulse = SendPulse()
        registros = Registro.query.filter(Registro.esta_no_bot == True).all()
        agora = datetime.now()
        quinze_minutos_atras = agora - timedelta(minutes=15)
        for i, registro in enumerate(registros):
            # verificando se o telefone está atribuido a alguém
            atribuido = sendpulse.obter_atribuicao(int(registro.telefone))
            if atribuido:
                db.session.delete(registro)
                db.session.commit()
            # verificando se houve duas ou mais mensagens enviadas ao usuário
            elif registro.quantidade_tentativas >= 2:
                sendpulse.acionar_fluxo(ID_FLUXO, registro.contact_id)
                print(f'Enviado menssagem para {registro.telefone}')
                db.session.delete(registro)
                db.session.commit()
            # verificando se está entre 07 e 19h
            elif registro.criado_em < quinze_minutos_atras and (agora.hour >= 7 and agora.hour <= 19):
                try:
                    sendpulse.enviar_mensagem_whatsapp(registro.telefone, LISTA_MENSAGENS[i])
                    print(f'Enviado menssagem para {registro.telefone}')
                    registro.quantidade_tentativas += 1
                    registro.contact_id = sendpulse.obter_contact_id(registro.telefone)
                    db.session.commit()
                except Exception as e:
                    print(f'Erro: {e}')
            print(f'Verificado(s) {i+1}/{len(registros)}')
        print('finalizado a verificação!')
