import socket
import random
import threading
from ast import literal_eval
from os import getpid
from time import sleep

from message import Message
from message_queue import MessageQueue
from states import States

ip = "127.0.0.1"
port = random.randint(1024, 65535)

init_node_ip = "127.0.0.1"
init_node_port = 12349


class Node:

    def __init__(self, ip, port, init_node_ip, init_node_port):
        self.ip = ip
        self.port = port
        self.init_node_ip = init_node_ip
        self.init_node_port = init_node_port

        self.conn_socket = None
        self.previous_socket = None
        self.next_ip = None
        self.next_port = None
        self.next_socket = None

        self.__number_of_ids = None
        self.__number_of_processes = None
        self.__processes_addresses = None
        self.__id = None
        self.__state = States.ACTIVE
        self.__round = 1
        self.message_queue = MessageQueue()

    def run(self):
        print("[BEGIN INITILIZATION]", flush=True)
        self.create_con_socket()
        self.join_group()
        thread = threading.Thread(target=self.create_previous_socket)
        thread.start()
        self.connect_to_next_socket()
        thread.join()
        print("[END INITILIZATION]", flush=True)

        print("\n[BEGIN ELECTION]", flush=True)
        is_leader, addresses = self.run_election()
        print("[END ELECTION]", flush=True)

        # self.close_own_socket()
        self.close_socket_to_next()

        return is_leader, addresses, self.conn_socket

    def join_group(self):
        s = socket.socket()
        s.connect((self.init_node_ip, self.init_node_port))
        print("Connected to init node. Waiting to be allocated in ring...")
        s.send(str((self.ip, self.port)).encode())

        msg = s.recv(1024).decode()
        self.__number_of_processes, self.__number_of_ids = literal_eval(msg)

        msg = s.recv(1024).decode()
        processes_str_addresses, next_index = literal_eval(msg)
        self.__processes_addresses = list(map(lambda t: literal_eval(t), processes_str_addresses))
        self.next_ip, self.next_port = self.__processes_addresses[next_index]
        print(f"Connected to ring. The node in front of my is {self.next_ip}:{self.next_port}")
        s.close()

    def create_con_socket(self):
        self.conn_socket = socket.socket()
        self.conn_socket.bind((self.ip, self.port))
        self.conn_socket.listen(1)

    def create_previous_socket(self):
        print("waiting for connection...")
        self.previous_socket, addr = self.conn_socket.accept()
        print("Received connection on previous socket")

    def connect_to_next_socket(self):
        self.next_socket = socket.socket()
        while True:
            print(f"Trying to connect to {self.next_ip}:{self.next_port}")
            try:
                self.next_socket.connect((self.next_ip, self.next_port))
                print("Connected to next node")
                break
            except:
                sleep(0.1)

    def close_socket_to_next(self):
        self.next_socket.close()

    def close_own_socket(self):
        self.previous_socket.close()

    def write(self, message):
        self.next_socket.send(message.encode())

    def read(self):
        return self.previous_socket.recv(1024).decode()

    def send_message(self, message_object: Message):
        message = str(Message.to_tuple(message_object))
        self.next_socket.send(message.encode())
        print(f"Sent message: {message}", flush=True)

    def receive_message(self):
        if not self.message_queue.empty():
            return self.message_queue.get_new_message()
        message_str = self.previous_socket.recv(1024).decode()
        print(f"Received message: {message_str}", flush=True)
        for mes in message_str.split(")("):
            mes = mes.replace("(", "").replace(")", "")
            self.message_queue.add_message(Message.from_tuple(literal_eval(mes)))
        return self.message_queue.get_new_message()

    def generate_id(self) -> int:
        """
        o valor do ID é gerado aleatoriamente
        """
        return random.randint(1, self.__number_of_ids)

    def run_election(self) -> tuple[bool, list[tuple[str, int]]]:
        """
        Enviando a primeira mensagem para o processo adjacente
        """
        self.__id = self.generate_id()
        message = Message(self.__id, self.__round)
        self.send_message(message)

        """
        A execução só termina quando todo processo estiver no estado PASSIVE
        ou ter sido eleito como líder e quando não restarem mais mensagens na
        MESSAGE QUEUE

        O comportamento dos processos está descrito no Tópico 2.1 do artigo
        da pasta DATA
        """
        while True:
            message = self.receive_message()
            match self.__state:
                case States.PASSIVE:
                    message.hop += 1
                    self.send_message(message)
                    if message.get_round() == -1:
                        self.__round = -1
                        if self.message_queue.empty():
                            print(f"SRC: {getpid()} is not the leader.", flush=True)
                            return False, self.__processes_addresses
                        else:
                            raise Exception(f"The Message Queue of {getpid()} is not empty after the leader election!")
                case States.ACTIVE:
                    if message.get_round() == -1:
                        raise Exception(f"The process {getpid()} should not be ACTIVE after the leader election!")
                    if (
                        message.hop == self.__number_of_processes
                        and message.bit == True
                    ):
                        self.__state = States.LEADER
                        message = Message(self.__id, -1)
                        self.send_message(message)
                    elif (
                        message.hop == self.__number_of_processes
                        and message.bit == False
                    ):
                        self.__id = self.generate_id()
                        self.__round += 1
                        message = Message(self.__id, self.__round)
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) == (self.__id, self.__round)
                        and (message.hop < self.__number_of_processes)
                    ):
                        message.hop += 1
                        message.bit = False
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) > (self.__id, self.__round)
                    ):
                        self.__state = States.PASSIVE
                        message.hop += 1
                        self.send_message(message)
                    elif (
                        (message.get_id(), message.get_round()) < (self.__id, self.__round)
                    ):
                        pass
                case States.LEADER:
                    if self.message_queue.empty():
                        self.__round = -1
                        print(f"SRC: The leader is {getpid()}!", flush=True)
                        return True, self.__processes_addresses
                    else:
                        raise Exception(f"The Message Queue of {getpid()} is not empty after the leader election!")


if __name__ == "__main__":
    Node(ip, port, init_node_ip, init_node_port).run()
