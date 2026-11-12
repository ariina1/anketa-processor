import requests

class ServerNedostupen(Exception):
    pass

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 5

def _request(method, endpoint, **kwargs):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        if response.status_code >= 500:
            raise ServerNedostupen(f"Ошибка на сервере: {response.status_code}")
        return response
    except (requests.ConnectionError, requests.Timeout) as e:
        raise ServerNedostupen("Сервер недоступен")

def get_all_ankety():
    return _request("GET", "/anketi").json()

def get_anketa(nomer):
    response = _request("GET", f"/anketi/{nomer}")
    if response.status_code == 404:
        return None
    return response.json()

def check_mail(mail):
    response = _request("POST", "/proverka", json={"mail": mail})
    return response.json().get("prinyato", False)

def get_statistika():
    return _request("GET", "/statistika").json()