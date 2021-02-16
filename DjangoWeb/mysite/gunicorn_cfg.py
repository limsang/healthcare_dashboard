from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()

daemon = False
# 0.0.0.0는 "모든 IP 주소"-메타 주소 (즉, 자리 표시 자 주소)를 의미합니다.
# 127.0.0.1는 항상 로컬 컴퓨터를 가리키는 예약 된 주소입니다.
# 그것이 "localhost"라고 불리는 이유입니다.
# 동일한 시스템에서 실행중인 프로세스에만 도달 할 수 있습니다.
bind = '0.0.0.0:' + environ.get('PORT', '8000')

# max_requests = 1000
# max_requests_jitter = 100
# 업로드 가능한 최대 용량
# - default: 1M
# client_max_body_size = 256
# 클라이언트 버퍼 사이즈 (body 에 들어오는 사이즈)
# - default: 32bit-8K, 64bit-16K
# client_body_buffer_size = 1;


worker_class = 'gevent'
workers = max_workers() #(max_workers() * 2 ) + 1
timeout = 60
graceful_timeout = 30

# keepalive = 2

accesslog="access.log"
errlog="err.log"
# threads = 2

