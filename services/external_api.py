import requests
from dotenv import load_dotenv
import os
from app.models import Token
from datetime import datetime, timedelta
from app.models import db


load_dotenv()

class SendPulse():
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        

    def criar_token(self):
        url = 'https://api.sendpulse.com/oauth/access_token'

        params ={
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        response = requests.post(url, json=params)

        try:
            response.raise_for_status()
            data = response.json()
            token = Token(
                token=data.get('access_token'),
                expira_em=datetime.now() + timedelta(seconds=3600)
            )
            db.session.add(token)
            db.session.commit()
            return token
            
        except Exception as e:
            print(f'Erro: {e}')
            return None
    
    def obter_token_valido(self):
        token = Token.query.filter(Token.expira_em > datetime.now()).first()
        if token:
            return token.token
        
        # caso que não existe token válido
        token = self.criar_token()
        # verificando se houve falha durante a criação do token
        if not token:
            print('Erro durante a criação do token')
        else:
            return token.token
    
    def enviar_mensagem_whatsapp(self, telefone: str, message: str):
        url = 'https://api.sendpulse.com/whatsapp/contacts/sendByPhone'

        params = {
            'bot_id': '68f76df5e170f893bc0cdf3c',
            'phone': telefone,
            'message': {
                'type': 'text',
                'text': {
                    'body': message
                }
            }
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=params, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            print(data)
        except Exception as e:
            print(f'Erro: {e}')

