import os
import time
import subprocess
import threading

def contenedor_r(image_n, RunTime):
    process = subprocess.Popen(f"docker run --rm {image_n}",
                               shell = True)
    time.sleep(RunTime)
    process.terminate()

##Elmines el quantum de aqui(Adr)
def planf(commands):
    threads =[]
    for command, STime, RunTime in commands:
        thread = threading.Timer(STime, contenedor_r, 
                                args = (command,RunTime))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(threads)

    # while commands:
    #     command = commands.pop(0)
    #     print(f"Running: {command}")
    #     process = subprocess.Popen(command, shell=True)
    #     time.sleep(quantum)
    #     process.terminate()
    #     commands.append(command)

def planificador_run(commands):
    commands_here = [(f"custom_container_image_{i}", int(STime), int(RunTime)) for i,(command, STime, RunTime) in enumerate(commands)]
    planf(commands_here)

"""
if __name__ == "__main__":
    ar_commands = "commands.txt"
    with open(ar_commands, "r") as f:
        commands = [line.strip().split(",") for line in f]
        commands = [(f"custom_container_image_{i}", int(STime), int(RunTime)) for i,
                    (command, STime, RunTime) in enumerate(commands)]

    planf(commands)
"""

    ##Prueba para el planificador inicial
    # commands = [
    #     "docker run --rm custom_container_image_1",
    #     .............
    # ]
    # quantum = 5
    # planf(commands, quantum)