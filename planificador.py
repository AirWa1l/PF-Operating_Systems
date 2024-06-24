import os
import time
import subprocess
import threading

def execute_command(command, index):
    dockerfile_n = f"Dockerfile_{index}"
    image_n = f"custom_container_image_{index}"
    dockerfile_content = f"""
    FROM ubuntu:latest
    RUN apt-get update && apt-get install -y procps
    CMD {command}
    """
    with open(dockerfile_n, "w") as f:
        f.write(dockerfile_content)
    os.system(f"docker build -f {dockerfile_n} -t {image_n} .")
    os.system(f"docker run --rm {image_n}")


def contenedor_r(image_n, RunTime):
    process = subprocess.Popen(f"docker run --rm {image_n}", shell=True)
    time.sleep(RunTime)
    process.terminate()

def execute_command(command, RunTime):
    contenedor_r(command, RunTime)

# FCFS Algorithm
def fcfs(commands):
    current_time = 0
    for command, arrival_time, burst_time in commands:
        if current_time < arrival_time:
            current_time = arrival_time
        thread = threading.Thread(target=execute_command, args=(command, burst_time))
        thread.start()
        thread.join(burst_time)
        turnaround_time = current_time + burst_time - arrival_time
        response_time = current_time - arrival_time
        print(f"FCFS - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
        current_time += burst_time

# SPN Algorithm
def spn(commands):
    current_time = 0
    queue = []
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            queue.sort(key=lambda x: x[2])  # Sort by burst time
            command, arrival_time, burst_time = queue.pop(0)
            thread = threading.Thread(target=execute_command, args=(command, burst_time))
            thread.start()
            thread.join(burst_time)
            turnaround_time = current_time + burst_time - arrival_time
            response_time = current_time - arrival_time
            print(f"SPN - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += burst_time
        else:
            current_time += 1

# SRT Algorithm
def srt(commands):
    current_time = 0
    queue = []
    burst_times = {i: burst_time for i, (_, _, burst_time) in enumerate(commands)}
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            queue.sort(key=lambda x: burst_times[x[0]])  # Sort by remaining burst time
            command, arrival_time, burst_time = queue.pop(0)
            index = list(burst_times.keys())[list(burst_times.values()).index(burst_time)]
            quantum = 1  # We use quantum = 1 to simulate SRT
            thread = threading.Thread(target=execute_command, args=(command, quantum))
            thread.start()
            thread.join(quantum)
            remaining_time = burst_time - quantum
            if remaining_time > 0:
                queue.append((command, arrival_time, remaining_time))
                burst_times[index] -= quantum
            else:
                turnaround_time = current_time + burst_time - arrival_time
                response_time = current_time - arrival_time
                print(f"SRT - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += quantum
        else:
            current_time += 1

# HRRN Algorithm
def hrrn(commands):
    current_time = 0
    queue = []
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            response_ratios = [(current_time - arrival_time + burst_time) / burst_time for _, arrival_time, burst_time in queue]
            index = response_ratios.index(max(response_ratios))
            command, arrival_time, burst_time = queue.pop(index)
            thread = threading.Thread(target=execute_command, args=(command, burst_time))
            thread.start()
            thread.join(burst_time)
            turnaround_time = current_time + burst_time - arrival_time
            response_time = current_time - arrival_time
            print(f"HRRN - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += burst_time
        else:
            current_time += 1

# Round Robin Algorithm
def round_robin(commands, quantum=2):
    current_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    queue = []
    response_times = {}
    burst_times = {i: burst_time for i, (_, _, burst_time) in enumerate(commands)}
    
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        
        if queue:
            command, arrival_time, burst_time = queue.pop(0)
            index = list(burst_times.keys())[list(burst_times.values()).index(burst_time)]
            if burst_time > quantum:
                thread = threading.Thread(target=execute_command, args=(command, quantum))
                thread.start()
                thread.join(quantum)
                remaining_time = burst_time - quantum
                queue.append((command, arrival_time, remaining_time))
                burst_times[index] -= quantum
                if index not in response_times:
                    response_times[index] = current_time - arrival_time
                current_time += quantum
            else:
                thread = threading.Thread(target=execute_command, args=(command, burst_time))
                thread.start()
                thread.join(burst_time)
                turnaround_time = current_time + burst_time - arrival_time
                response_time = response_times.get(index, current_time - arrival_time)
                total_turnaround_time += turnaround_time
                total_response_time += response_time
                print(f"Round Robin - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
                current_time += burst_time
        else:
            current_time += 1
    
    avg_turnaround_time = total_turnaround_time / len(burst_times)
    avg_response_time = total_response_time / len(burst_times)
    print(f"Round Robin - Average Turnaround Time: {avg_turnaround_time}, Average Response Time: {avg_response_time}")
    return avg_turnaround_time, avg_response_time

# Planificador principal
## Modificar la parte de algoritmo = 'fcfs' para que reciba una lista dinamica de los algoritmos y el elegido
def planificador_run(commands, algoritmo='fcfs', quantum=2):
    formatted_commands = [(command[0], int(command[1]), int(command[2])) for command in commands]
    if algoritmo == 'fcfs':
        fcfs(formatted_commands)
    elif algoritmo == 'spn':
        spn(formatted_commands)
    elif algoritmo == 'srt':
        srt(formatted_commands)
    elif algoritmo == 'hrrn':
        hrrn(formatted_commands)
    elif algoritmo == 'round_robin':
        round_robin(formatted_commands, quantum)
    else:
        print("Algoritmo no soportado.")


# ##Elmines el quantum de aqui(Adr)
# def planf(commands):
#     threads =[]
#     for command, STime, RunTime in commands:
#         thread = threading.Timer(STime, contenedor_r, 
#                                 args = (command,RunTime))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()
#     print(threads)

# def planificador_run(commands):
#     commands_here = [(f"custom_container_image_{i}", int(STime), int(RunTime)) for i,(command, STime, RunTime) in enumerate(commands)]
#     # planf(commands_here)

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