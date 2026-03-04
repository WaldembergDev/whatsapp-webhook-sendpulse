from wsgiref import headers
import requests
from dotenv import load_dotenv
import os
from app.models import Token
from datetime import datetime, timedelta
from app.models import db
from pprint import pprint


load_dotenv()

class SendPulse():
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.bot_id = os.getenv('BOT_ID')
        

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
                expira_em=datetime.now() + timedelta(seconds=3300)
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
            'bot_id': self.bot_id,
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
    

    def obter_contact_id(self, telefone: str):
        url = 'https://api.sendpulse.com/whatsapp/contacts/getByPhone'

        params = {
            'phone': telefone,
            'bot_id': self.bot_id
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, params=params, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            if not data:
                print('Dados vazios')
                return
            contact_id = data.get('data').get('id')
            return contact_id
        except Exception as e:
            print(f'Erro: {e}')
            return 
    

    def acionar_fluxo(self, flow_id: int, contact_id: str):
        url = 'https://api.sendpulse.com/whatsapp/flows/run'

        payload = {
            'flow_id': flow_id,
            'contact_id': contact_id
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            print(data)
            return 
        except Exception as e:
            print(f'Erro: {e}')
            return
    
    def fechar_chat(self, contact_id: str):
        url = 'https://api.sendpulse.com/whatsapp/contacts/closeChat'

        payload = {
            'contact_id': contact_id
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            print(data)
            return
        except Exception as e:
            print(f'Erro: {e}')
            return
    

    def obter_atribuicao(self, telefone: int):
        url = 'https://api.sendpulse.com/whatsapp/chats'

        params = {
            'bot_id': self.bot_id
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, params=params, headers=headers)

        atribuido = False

        try:
            response.raise_for_status()
            data = response.json()
            for valor in data.get('data'):
                telefone_encontrado = valor.get('contact').get('channel_data').get('phone')
                if telefone_encontrado == telefone:
                    atribuicao = valor.get('contact').get('operator')
                    if not atribuicao is None:
                        atribuido = True
                    return atribuido
            return atribuido
        except Exception as e:
            print(f'Erro: {e}')
            return False
        
    
    def definir_nome(self, contact_id: str, name: str):
        url = 'https://api.sendpulse.com/whatsapp/contacts/setName'

        payload = {
            'contact_id': contact_id,
            'name': name
        }

        headers = {
            'Authorization': f'Bearer {self.obter_token_valido()}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json=payload, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f'Erro: {e}')
            return
