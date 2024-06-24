import sys
from contenedor import container_run
from planificador import planificador_run

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Error: not enough parameters. Usage: main.py container <commands_file> planner <algorithm>")
        sys.exit(1)
    container = sys.argv[1]
    planner = sys.argv[3]

    if container == "container":

        commands = container_run()

    if planner == "planner":
        algorithm = sys.argv[4] if len(sys.argv) > 4 else 'fcfs'
        quantum = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        planificador_run(commands=commands, algoritmo=algorithm, quantum=quantum)


# if __name__ == "__main__":
#     print(sys.argv)
#     if 1 < len(sys.argv) < 3:
#         print("Error: not parameter digited, need to put main.py container planner")
#         sys.exit(1)
#     container = sys.argv[1]
#     planner = sys.argv[3]

#     if container == "container":

#         commands = container_run()

#     if planner == "planner":

#         planificador_run(commands=commands)
    