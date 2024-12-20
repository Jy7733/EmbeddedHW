# Cool SMS API 연동 
import json
import time
import datetime
import uuid
import hmac
import hashlib
import requests
import platform

from test_data import location,info

# 아래 값은 필요시 수정
protocol = 'https'
domain = 'api.coolsms.co.kr'
prefix = ''


def unique_id():
    return str(uuid.uuid1().hex)


def get_iso_datetime():
    utc_offset_sec = time.altzone if time.localtime().tm_isdst else time.timezone
    utc_offset = datetime.timedelta(seconds=-utc_offset_sec)
    return datetime.datetime.now().replace(tzinfo=datetime.timezone(offset=utc_offset)).isoformat()


def get_signature(key, msg):
    return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()


def get_headers(api_key, api_secret):
    date = get_iso_datetime()
    salt = unique_id()
    combined_string = date + salt

    return {
        'Authorization': 'HMAC-SHA256 ApiKey=' + api_key + ', Date=' + date + ', salt=' + salt + ', signature=' +
                         get_signature(api_secret, combined_string),
        'Content-Type': 'application/json; charset=utf-8'
    }


def get_url(path):
    url = '%s://%s' % (protocol, domain)
    if prefix != '':
        url = url + prefix
    url = url + path
    return url


def send_many(parameter):
    # 반드시 관리 콘솔 내 발급 받으신 API KEY, API SECRET KEY를 입력해주세요
    # api_key = 'NCSSYOLLGDWST5SY'
    # api_secret = 'HF7XYPDTHO9FJAGCAURDLKRKO1LJQGZ6'
    parameter['agent'] = {
        'sdkVersion': 'python/4.2.0',
        'osPlatform': platform.platform() + " | " + platform.python_version()
    }

    return requests.post(get_url('/messages/v4/send-many'), headers=get_headers(api_key, api_secret), json=parameter)



def send_sms(location, info) :
    data = {
        'messages': [
            {
                'to': '01041481902',
                'from': '01067034802',
                'text': "위치 정보 : " + location + "\n" + "이상 상태 감지 : " + info
            }
        ]
    }
    res = send_many(data)
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))
