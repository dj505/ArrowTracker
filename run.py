from app import create_app
from flask_apscheduler import APScheduler
from weekly import randomize_weekly

class Config(object):
    SCHEDULER_API_ENABLED = True

scheduler = APScheduler()
app = create_app()

@scheduler.task('cron', id='job', week='*', day_of_week='fri', hour='17', minute='53')
def job():
    randomize_weekly(app)

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
