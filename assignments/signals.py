from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin.messaging import Message,Notification
# from fcm_django.models import FCMDevice
from .models import Assignment,CustomDevice

@receiver(post_save, sender=Assignment)
def notify_assignment_created(sender, instance, created, **kwargs):
    if created:
        # Assuming Assignment has faculty, semester, subject fields
        faculty = instance.faculty
        semester = instance.semester
        subject = instance.subject

        # Assuming FCMDevice has a user field and user has faculty, semester, subject fields
        # devices = CustomDevice.objects.filter(
        #     user__faculty=faculty,
        #     user__semester=semester,
        #     user__subject=subject
        # )
        devices = CustomDevice.objects.all()
        # for device in devices:
        devices.send_message(
                Message(
                    notification=Notification(title="📘 New Assignment", body=f"{instance.title} ({subject}) has been added for {faculty}, Semester {semester}. Due on {instance.deadline.strftime('%Y-%m-%d')}"),
                    data={
                        "assignment_id": str(instance.assignment_id),
                        "faculty": str(faculty),
                        "semester": str(semester),
                        "subject": str(subject),
                        "route":"/getAssignment"
                    }
                )
            # message=f"Assignment '{instance.title}' for {subject} ({faculty}, Semester {semester}) is now available. Deadline: {instance.deadline.strftime('%Y-%m-%d')}",
            
        )
        #  if created:
    #     # Send notification to a topic instead of all devices
    #     FCMDevice.objects.send_message(
    #         title="📘 New Assignment",
    #         body=f"{instance.title} has been added. Due on {instance.deadline.strftime('%Y-%m-%d')}",
    #         data={"assignment_id": instance.id},
    #         topic="assignments"  # Specify your topic name here
    #     )
