# api/wsgi.py
import os, sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pass

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()  # a Vercel procura por "app"
