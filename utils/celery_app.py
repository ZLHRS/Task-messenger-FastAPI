from email.message import EmailMessage
from core.config import email_info, redis_url, celery_url
import aiosmtplib
import asyncio
from celery import Celery, shared_task

celery = Celery("tasks", broker=celery_url, backend=redis_url)

celery.conf.update(task_default_queue="celery", task_default_queue_type="classic")


async def send_email_task(to_email: str, title: str, body: str):

    message = EmailMessage()
    message["From"] = email_info.EMAIL_USERNAME
    message["To"] = to_email
    message["Subject"] = title
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=email_info.EMAIL_HOST,
        port=email_info.EMAIL_PORT,
        username=email_info.EMAIL_USERNAME,
        password=email_info.EMAIL_PASSWORD,
        start_tls=True,
    )


@shared_task
def send_email_async(email_to: str, title: str, body: str):
    asyncio.run(send_email_task(email_to, title, body))
