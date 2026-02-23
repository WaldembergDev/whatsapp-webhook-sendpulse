from app import create_app
from flask_apscheduler import APScheduler
from scripts.verificar_bot import listar_registros_no_bot


app = create_app()

# configuração do Agendador
class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# função que será executada a cada 10 min
@scheduler.task('interval', id='do_job_1', minutes=2, misfire_grace_time=900)
def job1():
    with app.app_context():
        print('Iniciando a tarefa')
        listar_registros_no_bot()

if __name__ == '__main__':
    app.run(debug=False)

# após 15 min fazer uma pergunta se ele deseja continuar ou encerrar o atendimento