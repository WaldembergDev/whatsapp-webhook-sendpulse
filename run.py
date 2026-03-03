from app import create_app
from scripts.verificar_bot import listar_registros_no_bot
from apscheduler.schedulers.background import BackgroundScheduler
import atexit


app = create_app()

# configuração do Agendador
scheduler = BackgroundScheduler()

# configuração da tarefa
scheduler.add_job(func=listar_registros_no_bot, trigger='interval', minutes=15, misfire_grace_time=900)
scheduler.start()

# garante que o agendador pare quando o app for fechado
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=False)

# após 15 min fazer uma pergunta se ele deseja continuar ou encerrar o atendimento