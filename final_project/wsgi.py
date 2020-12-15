"""
WSGI config for final_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
from dj_static import Cling # <- 加入

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')

# application = get_wsgi_application()
application = Cling(get_wsgi_application()) # <- 修改