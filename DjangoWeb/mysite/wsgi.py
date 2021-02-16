"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/


WSGI Middleware Component 기능
호출된 URL에 대한 라우팅 기능
하나의 프로세스에서 다중 어플리케이션 동작하도록 처리
로드밸런싱
컨텐츠 전처리 ( 예 : XSLT stylesheets )

gunicorn --bind 0:8000 config.wsgi:application 와 같이 수행한다.
--bind 0:8000의 의미는 8000번 포트로 WSGI 서버를 수행한다는 의미이고
config.wsgi:application 은 WSGI 서버가 호출하는 WSGI 어플리케이션은 config/wsgi.py 파일의 application 이라는 의미이다.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()

# daemon=True
# workers=5
