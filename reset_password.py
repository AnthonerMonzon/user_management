"""
Script to reset a user's password.
Run with: python reset_password.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')
django.setup()

from users.models import User

def reset_password():
    username = input("Enter username: ")
    new_password = input("Enter new password: ")
    
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"✓ Password for '{username}' reset successfully!")
    except User.DoesNotExist:
        print(f"✗ User '{username}' does not exist")

if __name__ == '__main__':
    reset_password()
