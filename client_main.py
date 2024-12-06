
# 탐지하고 데이터를 보내는 역할에 정의될 코드임 !!!!!!! 

# socket_client.py에서 정의된 함수들을 import
from socket_client import process_and_send_data
from client_socket_connection import receive_location_data

# 서버 설정
SERVER_HOST = '127.0.0.1'  # 서버 IP 주소 (로컬 호스트 예시)
SERVER_PORT = 8080  # 서버 포트 번호

# 소켓 연결 해두기 & 위치 받아서 업데이트
client_socket = receive_location_data(SERVER_HOST, SERVER_PORT)

if client_socket:
    # 위치를 처리하고 서버에 데이터를 전송하는 함수 호출
    process_and_send_data(client_socket, SERVER_HOST, SERVER_PORT)
else:
    print("Failed to establish connection with the server.")
