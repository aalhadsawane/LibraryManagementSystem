import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms_project.settings')
django.setup()

from api.models import User

def create_test_users():
    # Create test member
    if not User.objects.filter(email='member@example.com').exists():
        member = User.objects.create_user(
            email='member@example.com',
            username='member',
            password='Member123',
            first_name='Test',
            last_name='Member',
            user_type='MEMBER'
        )
        print(f"Created member user: {member.email}, password: Member123")
    else:
        print("Member user already exists")

    # Create test staff
    if not User.objects.filter(email='staff@example.com').exists():
        staff = User.objects.create_user(
            email='staff@example.com',
            username='staff',
            password='Staff123',
            first_name='Test',
            last_name='Staff',
            user_type='STAFF'
        )
        print(f"Created staff user: {staff.email}, password: Staff123")
    else:
        print("Staff user already exists")

    # Create test admin
    if not User.objects.filter(email='admin@example.com').exists():
        admin = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='Admin123',
            first_name='Test',
            last_name='Admin',
            user_type='ADMIN',
            is_staff=True,  # For Django admin access
            is_superuser=False  # Not a superuser, just an admin user
        )
        print(f"Created admin user: {admin.email}, password: Admin123")
    else:
        print("Admin user already exists")

if __name__ == "__main__":
    print("Creating test users...")
    create_test_users()
    print("Done!") 