import requests

class UserSession:
    def __init__(self):
        self.token = None

    def authenticate(self, username, password):
        url = "http://localhost:3000/Usuarios/log-in"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json().get("token")#.get("Claims").get()
            self.id = response.json().get("token").get("Claims").get("user_id")
            self.nick_name = response.json().get("token").get("Claims").get("user_nickname")
            return True
        else:
            print("Authentication failed")
            return False

    def is_authenticated(self):
        return self.token is not None

    def get_user_executions(self):
        if not self.is_authenticated():
            print("User is not authenticated")
            return None

        url = f"http://localhost:3000/Usuarios/buscar/ejecuciones/{self.id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and response.get("success") == True:
            executions = response.json().get("Procesos")
            return executions
        else:
            print("Failed to fetch executions")
            return None
        
    def log_out(self):
        if not self.is_authenticated():
            print("User is not authenticated")
            return None
        url = "http://localhost:3000/Usuarios/log-out"

        response = requests.get(url)
        if response.json().get("success") == True and response.status_code == 200:
            print(response.json().get("message"))
            return True
        return None
    
    def set_execution(self):
        pass