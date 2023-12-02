from multiprocessing import Lock
from os import getpid
from time import sleep

from lib.process_ring import Process_Ring

# Variáveis globais compartilhadas
GLOBAL_LOCK = Lock()
PLATES_AVAILABLE = 0

# Variáveis globais não compartilhadas
N = 7
K = 5
TOTAL_PLATES = 10

"""
O processo que não é líder vai tentar comer enquanto houverrem pratos
disponíveis feitos pelo processo líder
"""
def worker_function():
    plates_eaten = 0
    while PLATES_AVAILABLE > 0:
        with GLOBAL_LOCK:
            print(f"SRC: O processo {getpid()} está comendo...", flush=True)
            PLATES_AVAILABLE -= 1
        sleep(0.1)
        print(f"SRC: O processo {getpid()} terminou de comer!", flush=True)
        plates_eaten += 1
    
    print(f"SRC: O processo {getpid()} comeu {plates_eaten} pratos.", flush=True)
    return

"""
O processo líder regula quantos processos terão acesso aos pratos
"""
def leader_function():
    plates_cooked = 0
    for i in range(TOTAL_PLATES):
        print(f"SRC: O processo {getpid()} irá cozinhar!", flush=True)
        sleep(0.05)
        with GLOBAL_LOCK:
            print(f"SRC: O processo {getpid()} cozinhou mais um prato!", flush=True)
            PLATES_AVAILABLE += 1
        plates_cooked += 1
    print(f"SRC: O processo {getpid()} cozinhou {plates_cooked} pratos.", flush=True)
    return

def application():
    process_ring = Process_Ring(K, N, worker_function, leader_function)
    process_ring.run()