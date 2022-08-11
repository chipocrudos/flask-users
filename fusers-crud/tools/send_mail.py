from config import Configuration, loop, mail
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(template, subject, user, **kwargs):

    app = current_app._get_current_object()

    body = render_template(
                f"/mail/{template}.html",
                **kwargs
            )
    msg = Message(
        subject,
        sender=Configuration.DONT_REPLY_FROM_EMAIL,
        recipients=[user.email]
        )
    msg.html = body
    loop.run_in_executor(None, send_async_email, app, msg)
