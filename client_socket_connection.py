import socket
import time

# 서버와 연결하여 위치 데이터 수신 및 업데이트하는 함수
def receive_location_data(SERVER_HOST, SERVER_PORT):
    try:
        # 서버와 소켓 연결
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        while True:
            # 서버로부터 위치 데이터 받기
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Received from server: {data}")

                # 서버에서 받은 latitude, longitude 값을 target_lat, target_lon에 저장
                parts = data.split(", ")
                target_lat = float(parts[0].split(": ")[1])
                target_lon = float(parts[1].split(": ")[1])

                print(f"Updated target Latitude: {target_lat}, Target Longitude: {target_lon}")

            time.sleep(1)

        return client_socket  # 소켓 객체 반환

    except Exception as e:
        print(f"Error while receiving data: {e}")
        return None
