from flask import Flask
from tasks import crawl

flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_BROKER_URL='amqp://localhost',
    CELERY_RESULT_BACKEND='amqp://localhost'
)


@flask_app.route('/')
def hello_world():
    return 'Hello World!'


@flask_app.route('/pull')
def pull():
    crawl.delay()
    return "Pull!"


if __name__ == '__main__':
    flask_app.run()
