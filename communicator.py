import requests

class Communicator:
    def __init__(self):
        pass

    def on_login(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        response = requests.post("https://127.0.0.1:5000/login", form, verify=False)
        if(response.status_code != 202):
            #HANDLE INVALID CREDENTIALS :)
            return None
        print(response.json()["token"])
        return response.json()

    def on_register(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        response = requests.post("https://127.0.0.1:5000/login", form)
        print(response.json())
        return response.json()

    def on_post(self, symbol):
        form = {"input": symbol}
        response = requests.post("https://127.0.0.1:5000/login", form)
        print(response.json())
        return response.json()

    def get_status(self, token):
        form = {"token": token}
        response = requests.get("https://127.0.0.1:5000/status", form)
        print(response.json())
        return response.json()