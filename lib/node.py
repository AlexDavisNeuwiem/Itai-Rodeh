import socket
import random
import threading
from ast import literal_eval
from time import sleep

ip = "127.0.0.1"
port = random.randint(1024, 65535)

init_node_ip = "127.0.0.1"
init_node_port = 12347

     
class Node:
    
    def __init__(self, ip, port, init_node_ip, init_node_port):
        self.ip = ip
        self.port = port
        self.init_node_ip = init_node_ip
        self.init_node_port = init_node_port
        
        self.own_socket = None
        self.next_ip = None
        self.next_port = None
        self.next_socket = None
        
    def run(self):
        self.join_group()
        thread = threading.Thread(target=self.create_own_socket)
        thread.start()
        self.connect_to_next_socket()
        self.send_message(f"Hello, I am node {self.ip}:{self.port}")
        thread.join()
        self.close_own_socket()
        self.close_socket_to_next()
        
        
    def join_group(self):
        s = socket.socket()         
        s.connect((self.init_node_ip, self.init_node_port))
        s.send(str((self.ip, self.port)).encode()) 
        print (s.recv(1024).decode())
        self.next_ip, self.next_port = literal_eval(s.recv(1024).decode())
        print (f"The node in front of my is {self.next_ip}:{self.next_port}")
        s.close()
        
    def create_own_socket(self):
        s = socket.socket()         
        s.bind((self.ip, self.port))         
        s.listen(1)
        print("waiting for connection...")
        self.own_socket, addr =  s.accept()
        print("Received connection on own socket")
        print("Received message:", self.receive_message())
        
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
        self.own_socket.close()
        
    def send_message(self, message):
        self.next_socket.send(message.encode())
        
    def receive_message(self):
        return self.own_socket.recv(1024).decode()
        

if __name__ == "__main__":
    Node(ip, port, init_node_ip, init_node_port).run()
    