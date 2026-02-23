
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
