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
def fcfs(commands,dict_of_images):
    avg_turnaround = 0
    avg_response = 0
    turnaround_time_list = []
    response_time_list = []
    current_time = 0
    #i = 0
    for command, arrival_time, burst_time in commands:
        if current_time < arrival_time:
            current_time = arrival_time
        #image_n = f"custom_container_image_{i}"
        thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0], burst_time)) # args=(command, burst_time)
        thread.start()
        thread.join(burst_time)
        turnaround_time = current_time + burst_time - arrival_time
        response_time = current_time - arrival_time
        turnaround_time_list.append(turnaround_time)
        response_time_list.append(response_time)
        avg_turnaround += turnaround_time # Increment the value for then calculate the average
        avg_response += response_time
        print(f"FCFS - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
        current_time += burst_time
        #i += 1
    avg_turnaround_r = round(avg_turnaround / len(commands),3)
    avg_response_r = round(avg_response / len(commands),3)

    print(f"average turnaround times: {avg_turnaround_r}")
    print(f"average response times: {avg_response_r}")

    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround_r, 'average response times':avg_response_r}
    return dict_to_return

# SPN Algorithm
def spn(commands,dict_of_images):
    current_time = 0
    queue = []
    turnaround_time_list = []
    response_time_list = []
    avg_turnaround = 0
    avg_response = 0
    commands_copy = commands.copy()
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            queue.sort(key=lambda x: x[2])  # Sort by burst time
            command, arrival_time, burst_time = queue.pop(0)
            thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0], burst_time))
            thread.start()
            thread.join(burst_time)
            turnaround_time = current_time + burst_time - arrival_time
            response_time = current_time - arrival_time
            turnaround_time_list.append(turnaround_time)
            response_time_list.append(response_time)
            avg_turnaround += turnaround_time # Increment the value for then calculate the average
            avg_response += response_time
            print(f"SPN - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += burst_time
        else:
            current_time += 1
    avg_turnaround_r = round(avg_turnaround / len(commands_copy),3)
    avg_response_r = round(avg_response / len(commands_copy),3)

    print(f"average turnaround times: {avg_turnaround_r}")
    print(f"average response times: {avg_response_r}")

    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround_r, 'average response times':avg_response_r}
    return dict_to_return

# SRT Algorithm
def srt(commands,dict_of_images):
    current_time = 0
    queue = []
    turnaround_time_list = []
    response_time_list = []
    avg_turnaround = 0
    avg_response = 0
    commands_copy = commands.copy()
    burst_times = {i: burst_time for i, (_, _, burst_time) in enumerate(commands)}
    while commands or queue:
        i = 0
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            #print(burst_times)
            queue.sort(key=lambda x: burst_times[i])  # Sort by remaining burst time
            command, arrival_time, burst_time = queue.pop(0)
            index = list(burst_times.keys())[list(burst_times.values()).index(burst_time)]
            quantum = 1  # We use quantum = 1 to simulate SRT
            thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0], quantum))
            thread.start()
            thread.join(quantum)
            remaining_time = burst_time - quantum
            if remaining_time > 0:
                queue.append((command, arrival_time, remaining_time))
                burst_times[index] -= quantum
            else:
                turnaround_time = current_time + burst_time - arrival_time
                response_time = current_time - arrival_time
                turnaround_time_list.append(turnaround_time)
                response_time_list.append(response_time)
                avg_turnaround += turnaround_time # Increment the value for then calculate the average
                avg_response += response_time
                print(f"SRT - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += quantum
        else:
            current_time += 1
        
        i = 1
    avg_turnaround_r = round(avg_turnaround / len(commands_copy),3)
    avg_response_r = round(avg_response / len(commands_copy),3)

    print(f"average turnaround times: {avg_turnaround_r}")
    print(f"average response times: {avg_response_r}")

    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround_r, 'average response times':avg_response_r}
    return dict_to_return

# HRRN Algorithm -> 
def hrrn(commands,dict_of_images):
    current_time = 0
    queue = []
    turnaround_time_list = []
    response_time_list = []
    avg_turnaround = 0
    avg_response = 0
    commands_copy = commands.copy()
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        if queue:
            response_ratios = [(current_time - arrival_time + burst_time) / burst_time for _, arrival_time, burst_time in queue]
            index = response_ratios.index(max(response_ratios))
            command, arrival_time, burst_time = queue.pop(index)
            thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0], burst_time))
            thread.start()
            thread.join(burst_time)
            turnaround_time = current_time + burst_time - arrival_time
            response_time = current_time - arrival_time
            turnaround_time_list.append(turnaround_time)
            response_time_list.append(response_time)
            avg_turnaround += turnaround_time # Increment the value for then calculate the average
            avg_response += response_time
            print(f"HRRN - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
            current_time += burst_time
        else:
            current_time += 1
    avg_turnaround_r = round(avg_turnaround / len(commands_copy),3)
    avg_response_r = round(avg_response / len(commands_copy),3)

    print(f"average turnaround times: {avg_turnaround_r}")
    print(f"average response times: {avg_response_r}")

    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround_r, 'average response times':avg_response_r}
    return dict_to_return

# Round Robin Algorithm -> corregir round robin 
def round_robin(commands, dict_of_images, quantum=2):
    current_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    queue = []
    response_times = {}
    turnaround_time_list = []
    response_time_list = []
    burst_times = {i: burst_time for i, (_, _, burst_time) in enumerate(commands)}
    
    while commands or queue:
        while commands and commands[0][1] <= current_time:
            queue.append(commands.pop(0))
        
        if queue:
            command, arrival_time, burst_time = queue.pop(0)
            index = list(burst_times.keys())[list(burst_times.values()).index(burst_time)]
            if burst_time > quantum:
                #print(dict_of_images[command][0])
                thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0],quantum)) 
                thread.start()
                thread.join(quantum)
                remaining_time = burst_time - quantum
                queue.append((command, arrival_time, remaining_time))
                burst_times[index] -= quantum
                if index not in response_times:
                    response_times[index] = current_time - arrival_time
                current_time += quantum
            else:
                thread = threading.Thread(target=execute_command, args=(dict_of_images[command][0], burst_time))
                thread.start()
                thread.join(burst_time)
                turnaround_time = current_time + burst_time - arrival_time
                response_time = response_times.get(index, current_time - arrival_time)
                total_turnaround_time += turnaround_time
                total_response_time += response_time
                turnaround_time_list.append(turnaround_time)
                response_time_list.append(response_time)
                print(f"Round Robin - Command: {command}, Turnaround Time: {turnaround_time}, Response Time: {response_time}")
                current_time += burst_time
        else:
            current_time += 1
    
    avg_turnaround_time = total_turnaround_time / len(burst_times)
    avg_response_time = total_response_time / len(burst_times)

    print(f"average turnaround times: {avg_turnaround_time}")
    print(f"average response times: {avg_response_time}")

    dict_to_return = {'turnaround times' : turnaround_time_list, 'response times':response_time_list,'average turnaround times':avg_turnaround_time, 'average response times':avg_response_time}
    return dict_to_return

# Planificador principal
## Modificar la parte de algoritmo = 'fcfs' para que reciba una lista dinamica de los algoritmos y el elegido
def planificador_run(commands, images ,algoritmo='fcfs', quantum=2):
    formatted_commands = [(command[0], int(command[1]), int(command[2])) for command in commands]
    if algoritmo == 'fcfs':
        v = fcfs(formatted_commands,images)
        return v
    elif algoritmo == 'spn':
        v = spn(formatted_commands,images)
        return v
    elif algoritmo == 'srt':
        v = srt(formatted_commands,images)
        return v
    elif algoritmo == 'hrrn':
        v = hrrn(formatted_commands,images)
        return v
    elif algoritmo == 'round_robin':
        v = round_robin(formatted_commands, images,quantum)
        return v
    else:
        print("Algoritmo no soportado.")

