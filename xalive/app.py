from celery import Celery

app = Celery("xalive", include=["xalive.tasks"])

app.config_from_object("xalive.setting")

if __name__ == "__main__":
    app.start()