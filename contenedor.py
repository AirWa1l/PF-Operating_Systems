import os
import sys
from transform_list import transform_list


def c_dockerfile(command, index):
    dockerfile = f"""
    FROM ubuntu:latest
    RUN apt-get update && apt-get install -y procps
    CMD {command}
    """
    dockerfile_n = f"Dockerfile_{index}"
    with open(dockerfile_n, "w") as f:
        f.write(dockerfile)
    return dockerfile_n

def bar_container(dockerfile_n, image_n):
    os.system(f"docker build -f {dockerfile_n} -t {image_n} .")
    os.system(f"docker run --rm {image_n}")

def container_run():
    if len(sys.argv) < 3 or sys.argv[2] == "planner":
        print("Usage: main.py container <commands_file> planner <algorithm>")
        sys.exit(1)

    ar_commands = sys.argv[2]

    with open(ar_commands, "r") as f:
        commands = [line.strip() for line in f]
        
    commands = transform_list(commands)

    for i, command in enumerate(commands):
        dockerfile_n = c_dockerfile(command[0], i)
        image_n = f"custom_container_image_{i}"
        bar_container(dockerfile_n, image_n)

    return commands

"""
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python contenedor.py '<ar_commands>'")
        sys.exit(1)

    ar_commands = sys.argv[1]

    with open(ar_commands, "r") as f:
        commands = [line.strip() for line in f]
        
    commands = transform_list(commands)

    for i, command in enumerate(commands):
        dockerfile_n = c_dockerfile(command[0], i)
        image_n = f"custom_container_image_{i}"
        bar_container(dockerfile_n, image_n)

    ##Pruebas Iniciales, olvidar
    #command = sys.argv[1]
    #image_name = "custom_container_image"

    #c_dockerfile(command)
    #bar_container(image_name)

    print(commands)
"""
   