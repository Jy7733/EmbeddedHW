import socket
import time
import math
import serial


# 탐지 후 다른 라즈베리 파이에 전송하는 역할 
# 서버 주소 및 포트 설정
# SERVER_HOST = '192.168.1.2'  # 서버 IP 주소 (라즈베리파이 B)
SERVER_HOST = '127.0.0.1' #->로컬 ip (예시 )
SERVER_PORT = 8080  # 서버 포트 번호

# GPS 데이터 읽기 함수 (예시: 이전의 gps_read 함수)
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
    latitude = 0
    longtitude = 0
    return latitude, longtitude


# 두 지점 간의 거리를 계산하는 함수 (위도, 경도 기준)
def haversine(lat1, lon1, lat2, lon2):
    # R = 6371  # 지구 반지름 (킬로미터 단위)
    # phi1 = math.radians(lat1)
    # phi2 = math.radians(lat2)
    # delta_phi = math.radians(lat2 - lat1)
    # delta_lambda = math.radians(lon2 - lon1)

    # a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    # c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # distance = R * c  # 단위는 킬로미터

    # ---- 테스트용 더미 데이터 ------
    distance = 1
    return distance

# 특정 범위 내에 있는지 확인하는 함수
# km 는 바꿔야 할듯!!!!!!!!!!!!!!!!!!
def is_within_range(latitude, longitude, target_lat, target_lon, radius_km=10):
    distance = haversine(latitude, longitude, target_lat, target_lon)
    return distance <= radius_km

# 데이터 전송 함수
def send_data(latitude, longitude):
    try:
        # 서버와 소켓 연결
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_HOST, SERVER_PORT))

        # 전송할 데이터 준비
        data = f"Latitude: {latitude}, Longitude: {longitude}"

        # 서버에 데이터 전송
        client_socket.send(data.encode('utf-8'))

        # 서버로부터 응답 받기
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Server Response: {response}")

        # 연결 종료
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

# # GPS 데이터를 읽고 조건에 맞으면 서버에 데이터 전송
# def main():
#     # 라즈베리파이 B의 위치 (예시 데이터임! )
#     target_lat = 37.7749  # 예: 37.7749 (위도)
#     target_lon = -122.4194  # 예: -122.4194 (경도)

#     # 자신의 위치 읽기
#     latitude, longitude = gps_read()

#     # 범위 내에 있는지 확인
#     if is_within_range(latitude, longitude, target_lat, target_lon):
#         print(f"Latitude: {latitude}, Longitude: {longitude} is within range.")
#         send_data(latitude, longitude)
#     else:
#         print(f"Latitude: {latitude}, Longitude: {longitude} is out of range.")

# if __name__ == "__main__":
#     main()


# GPS 데이터를 읽고 조건에 맞으면 서버에 데이터 전송하는 함수
def process_and_send_data(client_socket, server_host, server_port):
    try:
        # 서버로부터 위치 데이터 받기
        data = client_socket.recv(1024).decode('utf-8')
        print(f"Received from server: {data}")

        # 서버에서 받은 latitude, longitude 값으로 target_lat, target_lon 설정
        parts = data.split(", ")
        target_lat = float(parts[0].split(": ")[1])
        target_lon = float(parts[1].split(": ")[1])

        print(f"Target Latitude: {target_lat}, Target Longitude: {target_lon}")

        # 자신의 위치 읽기
        latitude, longitude = gps_read()

        # 범위 내에 있는지 확인
        if is_within_range(latitude, longitude, target_lat, target_lon):
            print(f"Latitude: {latitude}, Longitude: {longitude} is within range.")
            send_data(latitude, longitude, server_host, server_port)
        else:
            print(f"Latitude: {latitude}, Longitude: {longitude} is out of range.")
    
    except Exception as e:
        print(f"Error while processing and sending data: {e}")
    
    except Exception as e:
        print(f"Error while processing and sending data: {e}")