from django.contrib.auth.management.commands.createsuperuser import Command as BaseCreateSuperUserCommand
from django.core.management.base import CommandError
from core.models import CustomUser

class Command(BaseCreateSuperUserCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)

        username = options.get('username') or input('Username: ')
        try:
            user = CustomUser.objects.get(username=username)
            user.role = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created with role='admin'"))
        except CustomUser.DoesNotExist:
            raise CommandError(f"User '{username}' not found to set role='admin'")
