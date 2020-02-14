from services import email_service
from tasks.queue import queue


@queue.celery.task()
def incoming_registration_notify(record_id, restaurant_name, owner_name, email, status, **kwargs):
    email_service.registration_notify(record_id, restaurant_name, owner_name, email, status)
    return record_id
