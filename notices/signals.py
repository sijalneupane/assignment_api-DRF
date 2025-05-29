from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Notices
from assignments.models import CustomDevice
from core.models import CustomUser  # adjust if needed
from fcm_django.admin import Notification,Message

@receiver(post_save, sender=Notices)
def notify_notice_saved(sender, instance, created, **kwargs):
    if created:
        if instance.target_audience == ["ALL"]:
            devices = CustomDevice.objects.all()
        else:
            # First, get user IDs whose faculty matches the target audience
            user_ids = CustomUser.objects.filter(faculty__in=instance.target_audience).values_list('id', flat=True)

            # Then, get devices for those users
            devices = CustomDevice.objects.filter(user_id__in=user_ids)

        # for device in devices:
        #     # send_notification(device, instance.title, instance.content)
        #     pass
        # devices.send_message(
        #     Message(
        #     notification=Notification(
        #         title="📢 New Notice",
        #         body=f"{instance.title}: {instance.content}"
        #     ),
        #     data={
        #         "notice_id": str(instance.id),
        #         "target_audience": str(instance.target_audience),
        #         "route": "/getNotice"
        #     }
        #     )
        # )
