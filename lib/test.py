from lib.itai_rodeh_process import Itai_Rodeh_Process
from lib.constants import Constants
from multiprocessing import Process

def test() -> None:
    N = int(input("N = "))
    K = int(input("K = "))
    Constants.number_of_processes = N
    Constants.number_of_ids = K

    itai_rodeh_process_list = [Itai_Rodeh_Process() for _ in range(N)]
    python_process_list = [Process(target=process.run) for process in itai_rodeh_process_list]
    for process in python_process_list:
        process.start()
        process.join()