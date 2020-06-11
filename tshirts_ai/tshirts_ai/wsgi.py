"""
WSGI config for tshirts_ai project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tshirts_ai.settings')

application = get_wsgi_application()
