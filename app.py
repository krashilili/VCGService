from flask import Flask
from tasks.tasks import add

flask_app = Flask(__name__)
# flask_app.config.update(
#     CELERY_BROKER_URL='amqp://localhost',
#     CELERY_RESULT_BACKEND='amqp://localhost'
# )


@flask_app.route('/')
def hello_world():
    return 'Hello World!'


@flask_app.route('/pull')
def pull():
    # vid, did, svid, ssid= "14e4", "163a", "105b", "0cff"
    kargs = {'vid': '14e4',
            'did': '163a',
            'svid': '105b',
            'ssid': '0cff'}
    # crawl.delay(**kargs)
    return "Pull!"


@flask_app.route('/add')
def add_one():
    add.delay(3,4)
    return "Done!"


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',port=5000)
