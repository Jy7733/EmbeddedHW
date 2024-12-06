# socket_client.py에서 정의된 함수들을 import
from socket_server import start_server

# 서버 설정
HOST = '0.0.0.0'  # 모든 인터페이스에서 연결 대기
PORT = 8080        # 포트 번호


# 위치를 처리하고 서버에 데이터를 전송하는 함수 호출
start_server(HOST,PORT)