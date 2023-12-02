from lib.process_ring import Process_Ring


def teste():
    process_ring = Process_Ring(3, 5, worker_function, leader_function)
    process_ring.run()

def worker_function():
    print("Estou trabalhando")

def leader_function():
    print("Estou fazendo a tarefa de um líder")