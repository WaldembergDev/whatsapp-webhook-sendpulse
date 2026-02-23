from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# após 15 min fazer uma pergunta se ele deseja continuar ou encerrar o atendimento