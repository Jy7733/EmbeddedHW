import socket
import threading
import time



# 자신의 위치 읽어오기 
def gps_read():
    # port = "/dev/ttyAMA0"  # GPS 모듈이 연결된 포트
    # baud_rate = 9600
    # ser = serial.Serial(port, baud_rate, timeout=1)

    # while True:
    #     data = ser.readline().decode('ascii', errors='ignore')
    #     if data:
    #         if "$GPRMC" in data:
    #             # GPS 데이터 파싱
    #             parts = data.split(",")
    #             latitude = parts[3]
    #             lat_direction = parts[4]
    #             longitude = parts[5]
    #             lon_direction = parts[6]

    #             latitude = float(latitude[:2]) + float(latitude[2:]) / 60
    #             if lat_direction == "S":
    #                 latitude = -latitude

    #             longitude = float(longitude[:3]) + float(longitude[3:]) / 60
    #             if lon_direction == "W":
    #                 longitude = -longitude

    #             return latitude, longitude
    #     time.sleep(1)
    
    
    # -------테스트용 더미 데이터 ------
    latitude = 1
    longtitude = 1
    return latitude, longtitude

# 클라이언트 연결을 처리하는 함수
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} established")
    
    # 클라이언트에게 연결 성공 메시지 전송
    client_socket.send("서버에 연결되었습니다. 위치 정보를 받기 시작합니다.".encode('utf-8'))

    # 주기적으로 위치 데이터를 전송
    try:
        while True:
            latitude, longitude = gps_read()  # GPS 데이터를 읽어옴
            data = f"Latitude: {latitude}, Longitude: {longitude}"  # 위치 정보 포맷팅

            # 클라이언트에게 위치 정보 전송
            client_socket.send(data.encode('utf-8'))
            print(f"Sent data to {client_address}: {data}")

            # 5초마다 위치 정보 전송
            time.sleep(5)

    except Exception as e:
        print(f"Error with client {client_address}: {e}")

    finally:
        # 연결 종료
        print(f"Closing connection with {client_address}")
        client_socket.close()

# 서버 소켓 설정
def start_server(HOST,PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
