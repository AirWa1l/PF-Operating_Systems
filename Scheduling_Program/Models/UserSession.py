import requests
import docker
import os

class UserSession:
    def __init__(self):
        self.token = None
        self.id = None
        self.nick_name = None
        self.client = docker.from_env()
    
    def register(self,nickname,email,password):
        url = "http://localhost:3000/Usuarios/crear"

        data = {"Nickname":nickname,"Email":email,"Password":password}
        response = requests.post(url=url,json=data)
        json = response.json()
        if response.status_code == 200 and json.get("Status") == 201:
            print("Register sucefully")
            return True
        return False


    def authenticate(self, username, password):
        url = "http://localhost:3000/Usuarios/log-in"
        data = {"email": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            self.token = response.json().get("tokenString")#.get("Claims").get()
            self.id = response.json().get("token").get("Claims").get("user_id")
            self.nick_name = response.json().get("token").get("Claims").get("user_nickname")
            print("Authentication accept")
            return True
        else:
            print("Authentication failed")
            return False
        

    def is_authenticated(self):
        if self.token == None:
            return False
        return True

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
        print(self.is_authenticated())
        if not self.is_authenticated():
            print("User is not authenticated")
            return False
        url = "http://localhost:3000/Usuarios/log-out"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }
        try:
            response = requests.get(url,cookies=cookies,headers=headers)
            print(f"HTTP Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    print(f"JSON Response: {json_response}")
                    if json_response.get("success"):
                        print(json_response.get("message"))
                        self.token = None  # Limpiar el token en el cliente
                        return True
                    else:
                        print("Logout failed. Success flag is false.")
                except ValueError:
                    print("Response is not in JSON format.")
            else:
                print("Logout request failed with status code:", response.status_code)
            return False
        
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return False
        #self.token = False
        """
        response = requests.get(url = url,headers=headers)
        
        #json = response.json()
        #print(json)
        if response.status_code == 200 :
            print(response.json())
            return True
        self.token = False
        return False
        """

    def get_image(self,command:str):

        url = "http://localhost:3000/Usuarios/buscar/imagen"

        data = {"id":self.id,"comando":command}

        response = requests.post(url=url, json=data)

        json = response.json()
        
        if response.status_code == 200 and json.get("success") == True and json.get("State") == 201:

            return (json.get("Image").get("imagen_id"),json.get("Image").get("imagen_name"),json.get("Image").get("imagen_used"))
        
        return False

    def set_image(self,process,imagen):
        
        # /Imagenes
        url = "http://localhost:3000/Imagenes/crear"

        data = {"pid":process[1],"imagen_id":imagen["imagen_id"],"imagen_used":imagen["imagen_used"],"imagen_name":imagen["imagen_name"]}

        response = requests.post(url=url,json=data)

        json = response.json()

        print(json.get("message"))

        if response.status_code == 200 and json.get("success") == True and json.get("State") == 201:
            return json.get("image_id")
        else:
            return False

    def evaluate_image_in_os(self,id):
        try:
            image = self.client.images.get(id)
            return True
        except docker.errors.ImageNotFound:
            return False
        
    def c_dockerfile(self,command):
        dockerfile_content = f"""
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD {command}
        """
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        dockerfiles_dir = os.path.join(project_root, "Dockerfiles")
        os.makedirs(dockerfiles_dir, exist_ok=True)  
        dockerfile_path = os.path.join(dockerfiles_dir, f"Dockerfile_{command}")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        return (dockerfile_path,f"Dockerfile_{command}:latest")
    
    def get_image_name_and_tag(self, image_id):

        try:
            image = self.client.images.get(image_id)
            for tag in image.tags:
                name, tag = tag.split(':')
                name_and_tag_tuple = (name, tag)
            return name_and_tag_tuple
        except docker.errors.ImageNotFound:
            print(f"Image with ID {image_id} not found")
            return None

    def build_image(self,path,tag):
        
        try:
            print(f"Building image from {path} with tag {tag}")
            image, _ = self.client.images.build(path=path, tag=tag)
            print(f"Image {tag} built successfully.")
            return image.id
        except docker.errors.BuildError as e:
            print(f"Error building image: {e}")
            return None

    def evaluate_images_in_os(self,data :dict):

        dict_to_return = {}
        for process,image in data.items():
            img = self.evaluate_image_in_os(image[0])

            if not img:
                dockerfile = c_dockerfile(process[0])

                image_id = self.build_image(path=dockerfile[0],tag=dockerfile[1])

                if image_id != None:
                    values = self.get_image_name_and_tag(image_id)

                    data = {"imagen_id":image_id,"imagen_used":values[1],"imagen_name":values[0]}

                reponse = self.set_image(process=process,imagen=data)

                if not reponse:
                    print("error")
                    return
                
                dict_to_return[process[0]] = (image_id,values[1],values[0])
            else:
                dict_to_return[process[0]] = (image[0],image[1],image[2])

        return dict_to_return

    def set_execution(self,processes:list):
        id_processes = []
        id_exec = 0
        dict_to_images_id = {}
        urlE = "http://localhost:3000/Usuarios/crear/ejecución"

        data = {"id":self.id}

        response = requests.post(url=urlE, json=data)

        json = response.json()

        if response.status_code == 200 and json.get("success") == True and json.get("State") == 201:

            id_exec = json.get("ID")


            urlP = "http://localhost:3000/Usuarios/crear/proceso"
            for command,time_start,time_estimated in processes:

                data = {"comando":command,"tiempo_inicio":time_start,"tiempo_estimado":time_estimated}

                response = requests.post(url=urlP,json=data)

                if response.status_code == 200 and response.json().get("success") == True and response.json().get("Status") == 201:

                    id_processes.append(response.json().get("ID"))

                    parameter = self.get_image(command)

                    dict_to_images_id[(command,response.json().get("ID"))] = parameter

                else:
                    print(response.json().get("message"))
                    return

        else:
            print(json.get("message"))
            return
        
        urlM = "http://localhost:3000/Usuarios/match/proceso_ejecución"

        for id in id_processes:
            
            data = {"pid":id,"eid":id_exec}

            response = requests.post(url=urlM,json=data)

            json = response.json()

            if response.status_code == 200 and json.get("succes") == True and json.get("State") == 201:

                print(json.get("message"))
                return True

            else:

                print(json.get("message")) 
                return
            
        dict_to_return =  self.evaluate_images_in_os(data=dict_to_images_id)

        return dict_to_return
        

def c_dockerfile(command, path):
        dockerfile_content = f"""
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD {command}
        """
        dockerfile_path = os.path.join(path, f"Dockerfile_{command}")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)
        return dockerfile_path

def build_image(path, tag, client):
        
        try:
            print(f"Building image from {path} with tag {tag}")
            image, _ = client.images.build(path=path, tag=tag)
            print(f"Image {tag} built successfully.")
            return image.id
        except docker.errors.BuildError as e:
            print(f"Error building image: {e}")
            return None


