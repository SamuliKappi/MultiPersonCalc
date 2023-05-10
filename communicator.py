import requests

class Communicator:
    def __init__(self):
        pass

    def on_login(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        try:
            response = requests.post("https://127.0.0.1:5000/login", form, verify=False)
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
        if(response.status_code != 202):
            return {"message": response.json["message"]}
        return response.json()

    def on_register(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        response = requests.post("https://127.0.0.1:5000/signup", form, verify=False)
        if(response.status_code != 201):
            return {"message": response.json["message"]}
        return response.json()

    def on_post(self, symbol, token):
        form = {"input": symbol, "token":token}
        response = requests.post("https://127.0.0.1:5000/addNumber", form, verify=False)
        if(response.status_code != 200):
            return {"message": response.json["message"]}
        return response.json()

    def on_reset(self, token):
        form = {"token": token}
        response = requests.post("https://127.0.0.1:5000/reset", form, verify=False)
        if(response.status_code != 200):
            return {"message": response.json["message"]}
        return response.json()
    
    def get_status(self, token):
        form = {"token": token}
        response = requests.get("https://127.0.0.1:5000/status", form, verify=False)
        if(response.status_code != 200):
            return {"message": response.json["message"]}
        return response.json()
    
    def equals(self, token):
        form = {"token": token}
        response = requests.post("https://127.0.0.1:5000/equals", form, verify=False)
        if(response.status_code != 200):
            return {"message": response.json["message"]}
        return response.json()