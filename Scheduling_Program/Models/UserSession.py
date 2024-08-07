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
            self.token = response.json().get("tokenString")
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

    def reused_user_executions(self,eid:int):

        dict_to_retorn = {}
        commands = []

        if not self.is_authenticated():
            print("User is not authenticated")
            return False
    
        url = "http://localhost:3000/Usuarios/reusar/ejecución"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        data = {"uid":self.id,"eid":eid}

        response = requests.post(url=url,headers=headers,cookies=cookies,json=data)

        json = response.json()

        if response.status_code == 200 and json.get("Status") == 200 and json.get("success") == True:

            temporal_dict = dict(json.get("Match")) 

            for key,value in temporal_dict.items():

                imagen_id = value["ImagenID"]
                imagen_used = value["ImagenUsed"]
                imagen_name = value["ImagenName"]

                new_value = (imagen_id,imagen_name,imagen_used)

                commands.append((value["Proceso"]["Comando"],value["Proceso"]["Tiempo_inicio"],value["Proceso"]["Tiempo_estimado"]))

                dict_to_retorn[key] = new_value

        return dict_to_retorn,commands
    
    def see_profile(self):

        url = f"http://localhost:3000/Usuarios/buscar/personal/{self.id}"


        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }
        
        response = requests.get(url = url, headers = headers, cookies = cookies)

        if response.json().get("State") == 200:

            return response.json().get("user")
    
        else:

            return False
    
    def delete_execution(self,id_exec):
        
        url = "http://localhost:3000/Usuarios/eliminar/ejecución"

        data = {"uid":self.id,"eid":id_exec}

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        response = requests.delete(url = url, json = data, cookies = cookies, headers = headers)

        if response.json().get("State") == 204 and response.json().get("success") == True:

            return True
        
        return False


    def update_profile(self,username = "default",email = "default",password = "default"):
        
        url = "http://localhost:3000/Usuarios/actualizar"

        data = {"id":self.id,"Nickname":username,"Email":email,"Password":password}

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        response = requests.put(url = url, headers = headers, cookies = cookies,json = data)
        return response.json().get("State") # StatusOK if update was okey

    def clean(self):

        url = "http://localhost:3000/Usuarios/eliminar/todo"

        data = {"id":self.id}

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        response = requests.delete(url = url, json = data, headers = headers, cookies = cookies)

        json = response.json()

        if response.status_code == 200 and json.get("State") == 204 and json.get("success") == True:

            return True

        return False

    def get_user_executions(self):
        if not self.is_authenticated():
            print("User is not authenticated")
            return False

        url = f"http://localhost:3000/Usuarios/buscar/ejecuciones/{self.id}"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        response = requests.get(url, headers=headers,cookies=cookies)

        if response.status_code == 200 and response.json().get("success") == True:
            executions = response.json().get("Procesos")

            return executions
        else:

            return False
        
    def log_out(self):
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
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if json_response.get("success"):
                        self.token = None  

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

    def get_image(self,command:str):

        url = "http://localhost:3000/Usuarios/buscar/imagen"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        data = {"id":self.id,"comando":command}

        response = requests.post(url=url, json=data,headers=headers,cookies=cookies)

        json = response.json()

        if response.status_code == 200 and json.get("success") == True and json.get("State") == 200:

            return (json.get("Image").get("ImagenID"),json.get("Image").get("ImagenName"),json.get("Image").get("ImagenUsed"))
        
        else:
            return False

    def set_image(self,process,imagen):
        
        url = "http://localhost:3000/Imagenes/crear"

        data = {"PID":process[1],"ImagenID":imagen["ImagenID"],"ImagenUsed":imagen["ImagenName"],"ImagenName":imagen["ImagenUsed"]}

        response = requests.post(url=url,json=data)

        json = response.json()

        if response.status_code == 200 and json.get("success") == True and json.get("State") == 201:
            return (json.get("image").get("ImagenID"),json.get("image").get("ImagenName"),json.get("image").get("ImagenUsed"))
        else:
            return False

    def evaluate_image_in_os(self,id):
        try:
            self.client.images.get(id)
            return True
        except docker.errors.ImageNotFound:
            return False
        
    def c_dockerfile(self,command):
        command_replace_spaces = ""
        dockerfile_content = f"""
        FROM ubuntu:latest
        RUN apt-get update && apt-get install -y procps
        CMD {command}
        """
        if command.find(" ") != -1:
            command_replace_spaces = command.replace(" ","")
        else:
            command_replace_spaces = command
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) 
        dockerfiles_dir = os.path.join(project_root, "Dockerfiles")
        os.makedirs(dockerfiles_dir, exist_ok=True)  
        dockerfile_path = os.path.join(dockerfiles_dir, f"dockerfile_{command_replace_spaces}")
        with open(dockerfile_path, "w") as f:
            f.write(dockerfile_content)

        return (dockerfiles_dir,f"dockerfile_{command_replace_spaces}",f"dockerfile_{command_replace_spaces}:latest")
    
    def get_image_name_and_tag(self, image_id):

        try:
            image = self.client.images.get(image_id)
            for tag in image.tags:
                name, tag = tag.split(':')
                name_and_tag_tuple = (name, tag)
            return name_and_tag_tuple
        except docker.errors.ImageNotFound:

            return None

    def build_image(self,path,dockerfile_name,tag):
        
        try:

            image, _ =  self.client.images.build(path=path, dockerfile=dockerfile_name, tag=tag)
            
            return image.id
        except docker.errors.BuildError as e:
            print(f"Error building image: {e}")
            return None

    def set_execution(self,processes:list,alg):
        id_processes = []
        id_exec = 0
        dict_to_images_id = {}

        urlE = "http://localhost:3000/Usuarios/crear/ejecución"

        data = {"id":self.id,"algorithm":alg}

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        cookies = {
            "token": self.token
        }

        response = requests.post(url=urlE, json=data,headers=headers,cookies=cookies)

        json = response.json()


        if response.status_code == 200 and json.get("success") == True and json.get("State") == 201:

            id_exec = json.get("ID")


            urlP = "http://localhost:3000/Usuarios/crear/proceso"
            for command,time_start,time_estimated in processes:

                data = {"comando":command,"tiempo_inicio":time_start,"tiempo_estimado":time_estimated}

                response = requests.post(url=urlP,json=data,headers=headers,cookies=cookies)

                json = response.json()


                if response.status_code == 200 and response.json().get("success") == True and response.json().get("Status") == 201:

                    id_processes.append(response.json().get("ID"))

                    parameter = self.get_image(command)


                    if parameter == False:


                        ruta,dockerfile,tag = self.c_dockerfile(command=command)

                        image_id = self.build_image(path=ruta,dockerfile_name=dockerfile,tag=tag)

                        if image_id != None:
                            values = self.get_image_name_and_tag(image_id)

                            pata = {"ImagenID":image_id,"ImagenUsed":values[1],"ImagenName":values[0]}
                        else:
                        
                            pata = {
                                "ImagenID":image_id,
                                "ImagenUsed":tag,
                                "ImagenName":dockerfile
                            }

                        parameter = self.set_image((command,response.json().get("ID")),pata)

                        dict_to_images_id[command] = parameter
                    
                    else:

                        dict_to_images_id[command] = parameter

                else:

                    return

        else:

            return
        
        urlM = "http://localhost:3000/Usuarios/match/proceso_ejecución"

        for id in id_processes:
            data = {"pid":id,"eid":id_exec}

            response = requests.post(url=urlM,json=data,headers=headers,cookies=cookies)

            json = response.json()

        return dict_to_images_id
    