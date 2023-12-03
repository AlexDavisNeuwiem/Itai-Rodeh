from os import getpid

from lib.process_ring import Process_Ring

N = 7
K = 5

def worker_function():
    print(f"SRC: {getpid()} is not the leader.", flush=True)
    return

def leader_function():
    print(f"SRC: The leader is {getpid()}!", flush=True)
    return

def application():
    process_ring = Process_Ring(K, N, worker_function, leader_function)
    process_ring.run()