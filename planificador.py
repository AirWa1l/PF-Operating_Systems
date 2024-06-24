import os
import time
import subprocess
import threading

def contenedor_r(image_n, RunTime):
    process = subprocess.Popen(f"docker run --rm {image_n}", shell=True)
    time.sleep(RunTime)
    process.terminate()

def execute_command(command, RunTime):
    contenedor_r(command, RunTime)

# FCFS Algorithm
def fcfs(commands):
    avg_turnaround = 0
    avg_response = 0
    turnaround_time_list = []
    response_time_list = []
    current_time = 0
    for command, arrival_time, burst_time in commands:
        if current_time < arrival_time:
            current_time = arrival_time
        thread = threading.Thread(target=execute_command, args=(command, burst_time))
        thread.start()
        thread.join(burst_time)
        turnaround_time = current_time + burst_time - arrival_time
        response_time = current_time - arrival_time
        turnaround_time_list.append(turnaround_time)
        response_time_list.append(response_time_list)
        avg_turnaround += turnaround_time # Increment the value for then calculate the average
        avg_response += response_time
        print(f"FCFS - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
        current_time += burst_time
    avg_turnaround = avg_turnaround / len(command)
    avg_response = avg_response / len(command)
    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround, 'average response times':avg_response}
    return dict_to_return

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

