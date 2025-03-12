import utils
import datetime
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def clear_credentials() -> None:
    app.logger.info("Clearing credentials")
    utils.delete_credentials()


@app.post('/api/v1/auth/login')
def login():
    credentials = request.json
    try:
        utils.initialize_credentials(
            credentials["aws_access_key_id"],
            credentials["aws_secret_access_key"],
            credentials["aws_region"]
        )
    except KeyError as e:
        return "Incorrect request body", 400
    app.logger.info("Credentials accepted")
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=5)
    scheduler.add_job(
        "delete credentials" + str(expires_at),
        func=clear_credentials,
        trigger='date',
        run_date=expires_at
    )
    return {'expires_at': expires_at}


@app.get('/api/v1/ecs/clusters')
def list_ecs_clusters():
    if utils.validate_credentials():
        return utils.list_ecs_clusters()
    else:
        return "Credentials expired, please log in again", 403


if __name__ == "__main__":
    app.run(port=6000, debug=True)
