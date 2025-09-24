from django.core.mail import send_mail
from django.conf import settings


def send_test_email(to_email: str) -> bool:
    """
    Надсилає тестовий лист на вказану адресу.
    """
    try:
        send_mail(
            subject='Перевірка пошти',
            message='Це тестовий лист для перевірки SMTP.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Помилка при надсиланні листа: {e}")
        return False
