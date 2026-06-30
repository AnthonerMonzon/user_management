"""
WSGI config for job_posting_site project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_posting_site.settings')

application = get_wsgi_application()
