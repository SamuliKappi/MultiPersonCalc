import requests

class Communicator:
    """
    Class Communicator uses requests library
    to send out HTTP requests to predetermined server
    """
    def __init__(self):
        pass

    def on_login(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        try:
            response = requests.post("https://127.0.0.1:5000/login", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 202):
            return {"error": response.json()["message"]}
        return response.json()

    def on_register(self, credentials):
        form = {"name": credentials[0], "password": credentials[1]}
        try:
          response = requests.post("https://127.0.0.1:5000/signup", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 201):
            return {"error": response.json()["message"]}
        return response.json()

    def on_post(self, symbol, token):
        form = {"input": symbol, "token":token}
        try:
          response = requests.post("https://127.0.0.1:5000/addNumber", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()

    def on_reset(self, token):
        form = {"token": token}
        try:
          response = requests.post("https://127.0.0.1:5000/reset", form, verify=False)
        except requests.exceptions.ConnectionError:
          return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()
    
    def get_status(self, token):
        form = {"token": token}
        try:
          response = requests.post("https://127.0.0.1:5000/status", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()
    
    def equals(self, token):
        form = {"token": token}
        try:
          response = requests.post("https://127.0.0.1:5000/equals", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()

    def swap(self, token):
        form = {"token": token}
        try:
          response = requests.post("https://127.0.0.1:5000/swap", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()

    def erase(self, token):
        form = {"token": token}
        try:
          response = requests.post("https://127.0.0.1:5000/erase", form, verify=False)
        except requests.exceptions.ConnectionError:
            return {"error": "Connection refused"}
        if(response.status_code != 200):
            return {"error": response.json()["message"]}
        return response.json()