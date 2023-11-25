from multiprocessing import Process

from lib.itai_rodeh_process import Itai_Rodeh_Process


def process_ring_initializer() -> None:
    # Obtendo o valor de N e K
    number_of_processes = int(input("N = "))
    number_of_ids = int(input("K = "))

    # Inicializando o ciclo de processos de Itai-Rodeh
    process_ring = [Itai_Rodeh_Process(number_of_ids, number_of_processes) for _ in range(number_of_processes)]

    # Gerando a lista de processos do sistema
    python_process_list = []
    for i in range(number_of_processes):
        next_ring_index = (i + 1) % number_of_processes
        python_process = Process(target=process_ring[i].run, args=(process_ring[next_ring_index],))
        python_process_list.append(python_process)

    # Iniciando a execução de cada processo
    for python_process in python_process_list:
        python_process.start()
        python_process.join()