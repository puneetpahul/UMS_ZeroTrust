from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Role, Department
import random
import string

class Command(BaseCommand):
    help = 'Seed database with custom users'

    def random_username(self, length):
        # Generate a random username of specified length using lowercase letters
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def handle(self, *args, **kwargs):
        User = get_user_model()
        staff_role = Role.objects.get_or_create(name='staff')[0]
        department4 = Department.objects.get_or_create(name='department4')[0]

        for i in range(0,3):  # Example: Create 10 users
            username_length = random.randint(5,7)
            username = self.random_username(username_length)+f'{i}'+ ".staff@gmail.com"
            user = User.objects.create(
                username=username,
                email=username,
                role=staff_role,
                department=department4,    ## Change department here
                country='PK',              ## Change country here 
                is_staff=False,
                is_superuser=False
            )
            user.set_password('defaultpassword')
            print(user.set_password(f'defaultpassword'),'**************')
            
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully created 100 custom users.'))
