from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
from weekly import randomize_weekly

class Config(object):
    SCHEDULER_API_ENABLED = True

scheduler = BackgroundScheduler()
app = create_app()

def job():
    randomize_weekly(app)

scheduler.add_job(job, 'cron', week='*', day_of_week='fri', hour='12')

if __name__ == '__main__':
    #scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)
