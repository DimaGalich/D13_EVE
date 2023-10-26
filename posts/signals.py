from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Reply



@receiver(post_save, sender=Reply)
def reply_announcer(sender, instance, created, **kwargs):
    message_1 = f'Новый отклик для "{instance.post.title}" пользователем {instance.author.name}'
    email_box_1 = instance.post.author.name.email

    print(message_1)
    print(f'Автор {instance.post.author} отправлено письмо на {email_box_1}')
    if created:
        send_mail(subject='Получен отклик',
                  message=message_1,
                  from_email=None,
                  recipient_list=[email_box_1, ])

    if instance.approved:
        message_2 = f'Отклик для "{instance.post.title}" принят автором {instance.post.author.name}'
        email_box_2 = instance.author.name.email

        send_mail(subject='Ваш отклик принят',
                  message=message_2,
                  from_email=None,
                  recipient_list=[email_box_2, ])
