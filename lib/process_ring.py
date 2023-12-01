from multiprocessing import Process

from lib.itai_rodeh_process import Itai_Rodeh_Process


class Process_Ring:
    def __init__(self, number_of_ids: int, number_of_processes: int) -> None:
        # Inicializando o ciclo de processos de Itai-Rodeh
        self.__process_ring = []
        for i in range(number_of_processes):
            itai_rodeh_process = Itai_Rodeh_Process(number_of_ids, number_of_processes)
            self.__process_ring.append(itai_rodeh_process)

        # Gerando a lista de processos do sistema
        self.__python_process_list = []
        for i in range(number_of_processes):
            next_ring_index = (i + 1) % number_of_processes
            python_process = Process(target=self.__process_ring[i].run, args=(self.__process_ring[next_ring_index],))
            self.__python_process_list.append(python_process)

    def run(self):
        # Iniciando a execução de cada processo
        for python_process in self.__python_process_list:
            python_process.start()

        # Realizando o join dos processos
        for python_process in self.__python_process_list:
            python_process.join()