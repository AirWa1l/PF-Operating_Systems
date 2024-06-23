import os
import sys

def c_dockerfile(command,index):
    dockerfile = f"""
    FROM ubuntu:latest
    RUN apt-get update && apt-get install -y procps
    CMD {command}
    """
    dockerfile_n = f"Dockerfile_{index}"
    with open(dockerfile_n,"w") as f:
        f.write(dockerfile)
    return dockerfile_n

def bar_container(dockerfile_n,image_n):
    os.system(f"docker build -f {dockerfile_n} -t {image_n} .")
    os.system(f"docker run --rm {image_n}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python contenedor.py '<ar_commands>'")
        sys.exit(1)

    ar_commands = sys.argv[1]

    with open(ar_commands, "r") as f:
        commands = [line.strip() for line in f]

    for i, command in enumerate(commands):
        dockerfile_n = c_dockerfile(command, i)
        image_n = f"custom_container_image_{i}"
        bar_container(dockerfile_n, image_n)

    ##Pruebas Iniciales, olvidar
    #command = sys.argv[1]
    #image_name = "custom_container_image"

    #c_dockerfile(command)
    #bar_container(image_name)