def save_user(username, password):
    try:
        with open("Usuarios.txt", "w") as newfile:
            newfile.write(username + "\n")
            newfile.write(password + "\n")
        return True
    except Exception as e:
        print(e)
        return False

def validate_user(username, password):
    try:
        with open("Usuarios.txt", "r") as file:
            stored_username = file.readline().strip()
            stored_password = file.readline().strip()
            return username == stored_username and password == stored_password
    except FileNotFoundError:
        return False
