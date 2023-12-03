import random
import socket
from time import sleep

from node import Node

ip = "127.0.0.1"
port = random.randint(1024, 65535)

init_node_ip = "127.0.0.1"
init_node_port = 12345


class ApplicationNode:

    def __init__(self, ip, port, init_node_ip, init_node_port):
        self.ip = ip
        self.port = port
        self.init_node_ip = init_node_ip
        self.init_node_port = init_node_port

        self.sockets = []

    def run(self):
        is_leader, nodes_addresses, conn_socket = Node(self.ip, self.port, self.init_node_ip, self.init_node_port).run()
        print("\n[APPLICATION]", flush=True)
        if is_leader:
            self.leader(nodes_addresses)
        else:
            self.follower(conn_socket)

    def leader(self, nodes_addresses):
        for ip, port in nodes_addresses:
            s = self.connect_to_socket(ip, port)
            self.sockets.append(s)
        while True:
            msg = input("Enter message to broadcast: ")
            self.broadcast(msg)

    def connect_to_socket(self, ip, port):
        while True:
            try:
                s = socket.socket()
                s.connect((ip, port))
                return s
            except:
                sleep(0.1)

    def follower(self, conn_socket):
        print("Wait for leader messages")
        own_socket, addr = conn_socket.accept()
        while True:
            msg = own_socket.recv(1024).decode()
            print("Received msg from leader: ", msg)

    def broadcast(self, msg):
        for s in self.sockets:
            s.send(msg.encode())


if __name__ == "__main__":
    ApplicationNode(ip, port, init_node_ip, init_node_port).run()
