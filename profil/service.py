from typing import Optional
from django.core.mail import send_mail


def sending_welcome_message_on_email_user(email_user: Optional[str]):
    send_mail(
        'Вітаємо з реєстрацією в нашому інтернет-магазині',
        'Ми будемо регулярно вас повідомляти про новинки в нашому інтернет-магазині',
        'vzaharkiv28@gmail.com',
        [email_user],
        fail_silently=False
    )
