from django.core.management.base import BaseCommand
from django.db.models import ObjectDoesNotExist

from apps.user.models import User, UserManager


class Command(BaseCommand):
    """Command for initializing data to user app: user"""
    help = 'Initialize default data: admin_user'

    def handle(self, *args, **options):
        self._create_admin_if_not_exist()

    def _create_admin_if_not_exist(self):
        admin_email = 'admin@example.com'
        admin_name = 'admin'

        try:
            admin = User.objects.get(email=admin_email, is_staff=True)

            self.stdout.write(self.style.SUCCESS(f'Administrator {admin} already exists'))
        except ObjectDoesNotExist:
            user_manager = UserManager()
            user_manager.model = User
            admin_data = dict(
                email=admin_email,
                password="admin1234",
                first_name=admin_name,
                last_name=admin_name
            )

            user_manager.create_superuser(**admin_data)

            self.stdout.write(
                self.style.SUCCESS(f"Administrator {admin_data['email']}  with password '{admin_data['password']}'")
            )
