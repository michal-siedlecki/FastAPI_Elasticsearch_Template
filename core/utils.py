import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict
import emails
from emails.template import JinjaTemplate
from core.config import settings

API_VERSION = settings.API_VERSION

async def send_email(
        email_to: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
) -> None:
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.MAIL_FROM_NAME, settings.MAIL_FROM),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


async def send_test_email(email_to: str) -> None:
    subject = f"Shappire - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email_test.html") as f:
        template_str = f.read()
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"title": "Shappire", "name": email_to},
    )


async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    subject = f"Shappire - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR), "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}{API_VERSION}/reset-password-form?token={token}"
    expire_at = (datetime.utcnow() + timedelta(minutes=int(settings.PASSWORD_RESET_TOKEN_EXPIRES_MINUTES))).strftime(
        "%H:%M:%S")
    await send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": "Shappire",
            "username": email,
            "email": email_to,
            "expiration_time": expire_at,
            "link": link
        }
    )


# def send_new_account_email(email_to: str, username: str, password: str) -> None:
#     subject = f"Shappire - New account for user {username}"
#     with open(Path(os.environ.get('EMAIL_TEMPLATES_DIR')) / "new_account.html") as f:
#         template_str = f.read()
#     link = os.environ.get('SERVER_HOST')
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "project_name": "Shappire",
#             "username": email_to,
#             "password": password,
#             "valid_minutes": os.environ.get("PASSWORD_RESET_TOKEN_EXPIRES_MINUTES"),
#             "link": link
#         }
#     )
