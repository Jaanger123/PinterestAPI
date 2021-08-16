from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_code(email, activation_code, status):
    if status == 'register':
        context = {
            'domain': 'http://localhost:8000',
            'activation_code': activation_code
        }
        msg_html = render_to_string('activate.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate your account',
            message,
            'pinterest@gmail.com',
            [email],
            html_message=msg_html,
            fail_silently=False
        )
    elif status == 'reset_password':
        context = {
            'activation_code': activation_code
        }
        msg_html = render_to_string('reset.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Reset your password',
            message,
            'pinterest@gmail.com',
            [email],
            html_message=msg_html,
            fail_silently=False
        )
