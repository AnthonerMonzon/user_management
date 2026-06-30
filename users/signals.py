"""
Django signals for user management with Supabase integration.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from .supabase_utils import sync_user_to_supabase


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for user creation/update.
    Syncs user to Supabase when created or updated.
    """
    if created:
        # Sync new user to Supabase
        sync_user_to_supabase(instance)
    # You can add update logic here if needed


@receiver(post_delete, sender=User)
def user_post_delete(sender, instance, **kwargs):
    """
    Signal handler for user deletion.
    Could be used to delete user from Supabase as well.
    """
    # Add Supabase deletion logic if needed
    pass
