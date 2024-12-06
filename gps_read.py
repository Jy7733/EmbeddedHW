import serial
import time

# 시리얼 포트 설정 (GPS 모듈이 연결된 포트명으로 변경)
port = "/dev/ttyAMA0"  # 라즈베리파이에서 사용되는 시리얼 포트
baud_rate = 9600  # GPS 모듈의 기본 Baud rate

# 시리얼 포트 열기
ser = serial.Serial(port, baud_rate, timeout=1)

# GPS 데이터를 읽고 위도, 경도를 파싱하는 함수
def parse_gps_data(data):
    if "$GPRMC" in data:
        try:
            parts = data.split(",")
            latitude = parts[3]
            lat_direction = parts[4]
            longitude = parts[5]
            lon_direction = parts[6]

            # 위도, 경도 계산 (위도와 경도는 N/S, E/W로 방향이 지정됨)
            latitude = float(latitude[:2]) + float(latitude[2:]) / 60
            if lat_direction == "S":
                latitude = -latitude

            longitude = float(longitude[:3]) + float(longitude[3:]) / 60
            if lon_direction == "W":
                longitude = -longitude

            return latitude, longitude
        except Exception as e:
            print("Error parsing GPS data:", e)
    return None, None

# GPS 데이터를 읽어오는 함수
def gps_read():
    while True:
        # GPS로부터 데이터 한 줄 읽기
        data = ser.readline().decode('ascii', errors='ignore')
        if data:
            print("Received data:", data)
            latitude, longitude = parse_gps_data(data)
            if latitude and longitude:
                print(f"Latitude: {latitude}, Longitude: {longitude}")
                return latitude, longitude
        time.sleep(1)
