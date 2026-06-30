"""
Supabase integration utilities for Django backend.
"""
import os
from supabase import create_client, Client
from django.conf import settings


def get_supabase_client() -> Client:
    """
    Get Supabase client instance.
    Make sure to set SUPABASE_URL and SUPABASE_KEY in your environment variables.
    """
    supabase_url = getattr(settings, 'SUPABASE_URL', os.environ.get('SUPABASE_URL', ''))
    supabase_key = getattr(settings, 'SUPABASE_KEY', os.environ.get('SUPABASE_KEY', ''))
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
    
    return create_client(supabase_url, supabase_key)


def sync_user_to_supabase(user):
    """
    Sync Django user to Supabase auth.
    This creates or updates a user in Supabase auth system.
    """
    try:
        supabase = get_supabase_client()
        
        # Try to create user in Supabase
        # Note: This requires the service role key for admin operations
        service_role_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', os.environ.get('SUPABASE_SERVICE_ROLE_KEY', ''))
        
        if service_role_key:
            admin_client = create_client(
                getattr(settings, 'SUPABASE_URL', os.environ.get('SUPABASE_URL', '')),
                service_role_key
            )
            
            # Create user in Supabase
            admin_client.auth.admin.create_user({
                'email': user.email,
                'password': 'temp_password_123',  # Should be handled properly in production
                'email_confirm': True,
                'user_metadata': {
                    'username': user.username,
                    'user_type': user.user_type,
                    'django_id': user.id
                }
            })
            
    except Exception as e:
        print(f"Error syncing user to Supabase: {e}")
        # Don't raise error to allow Django operations to continue
        pass


def get_supabase_user(email):
    """
    Get user from Supabase by email.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.auth.admin.get_user_by_email(email)
        return response.user
    except Exception as e:
        print(f"Error getting user from Supabase: {e}")
        return None
