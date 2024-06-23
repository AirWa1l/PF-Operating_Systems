import os
import time
import subprocess
import threading

def contenedor_r(image_n, RunTime):
    process = subprocess.Popen(f"docker run --rm{image_n}",
                               shell = True)
    time.sleep(RunTime)
    process.terminate()

def planf(commands, quantum):
    while commands:
        command = commands.pop(0)
        print(f"Running: {command}")
        process = subprocess.Popen(command, shell=True)
        time.sleep(quantum)
        process.terminate()
        commands.append(command)

if __name__ == "__main__":
    commands = [
        "docker run --rm custom_container_image_1",
        "docker run --rm custom_container_image_2",
        "docker run --rm custom_container_image_3",
    ]
    quantum = 5
    planf(commands, quantum)