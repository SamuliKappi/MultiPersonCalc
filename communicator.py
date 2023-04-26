import requests

class Communicator:
    def __init__(self):
        pass

    def on_login(self, credentials):
        payload = {"username": credentials[0], "password": credentials[1]}
        response = requests.post("https://127.0.0.1:5000/login", payload)
        print(response)
        return True

    def on_register(self, credentials):
        payload = {"username": credentials[0], "password": credentials[1]}
        response = requests.post("https://127.0.0.1:5000/login", payload)
        print(response)
        return True

    def on_post(self, symbol):
        payload = {"symbol": symbol}
        response = requests.post("https://127.0.0.1:5000/login", payload)
        print(response)
        return True

    def get_status(self):
        requests.get
        return update