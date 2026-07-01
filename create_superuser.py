"""
Script to create a superuser programmatically.
Run with: python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

from users.models import User

def create_superuser():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type=User.UserType.SUPERADMIN
        )
        print(f"✓ Superuser '{username}' created successfully!")
        print(f"  User type: {user.get_user_type_display()}")
    except Exception as e:
        print(f"✗ Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
