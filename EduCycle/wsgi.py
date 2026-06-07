"""
WSGI config for EduCycle project.
Runs Django migrations automatically on Vercel cold starts.
"""

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduCycle.settings')

# Auto-migrate on startup (required for Vercel serverless)
from django.core.management import call_command
try:
    call_command('migrate', '--noinput', verbosity=0)
except Exception as e:
    import traceback
    print(f"[WSGI] Migration error: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    err_msg = traceback.format_exc()
    def application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [err_msg.encode('utf-8')]
