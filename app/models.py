
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(16), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    esta_no_bot = db.Column(db.Boolean, default=True)
    quantidade_tentativas = db.Column(db.Integer, default=0)


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    expira_em = db.Column(db.DateTime, nullable=False)

    def __str__(self):
        return self.token
    
    def esta_expirado(self):
        agora = datetime.now()
        if agora > self.expira_em:
            return True
        return False