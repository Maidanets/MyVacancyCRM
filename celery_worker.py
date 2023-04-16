from celery import Celery
from email_lib import EmailWrapper
from models import EmailCredentials
import db_alchemy
import os

RABBIT_HOST = os.environ.get('RABBIT_HOST', 'localhost')
app = Celery('celery_worker', broker=f'pyamqp://guest@{RABBIT_HOST}//')


@app.task
def send_mail(id_email_creds, recipient, message):
    db_alchemy.init_db()
    email_creds_details = db_alchemy.db_session.query(EmailCredentials).get(id=id_email_creds)
    email_wrapper = EmailWrapper(**email_creds_details.get_mandatory_fields())
    email_wrapper.send_email(recipient, message)


