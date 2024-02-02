from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


"""
Email handler
"""

def email_sender(subject, message, to, extra=None):
    # from_email = 'your-email@gmail.com'
    recipient_list = [to,]
    html_body = render_to_string(template_name="email/email_temp.html", context={'message':message, 'extra':extra})

    message = EmailMultiAlternatives(
    subject=subject,
    body=message,
    from_email='From INFO',
    to=recipient_list
    )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=True)
    # send_mail(subject, message, from_email, recipient_list)
