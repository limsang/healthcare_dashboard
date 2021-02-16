#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


# WSGI is the main Python standard for communicating between Web servers and applications, but it only supports synchronous code.
# ASGI is the new, asynchronous-friendly standard that will allow your Django site to use asynchronous Python features, and asynchronous Django features as they are developed.

# 콘솔에서는 python manage.py runserver명령을 실행해, 웹 서버를 바로 시작할 수 있습니다.
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()