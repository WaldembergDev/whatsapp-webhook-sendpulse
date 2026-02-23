from flask import Flask
from .models import db
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # inicializa o banco com o app
    db.init_app(app)

    # registra op blueprint das rotas
    app.register_blueprint(main)

    # cria as tabelas se não existirem
    with app.app_context():
        db.create_all()

    return app

