from celery import Celery

app = Celery("xcraw", include=["xcraw.tasks"])

app.config_from_object("xcraw.setting")

if __name__ == "__main__":
    app.start()