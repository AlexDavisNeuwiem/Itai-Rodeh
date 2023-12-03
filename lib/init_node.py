import socket     

ip = "127.0.0.1"
port = 12347
clients_amount = 2    
 
class InitNode:
    
    def __init__(self, ip, port, clients_amount):
        self.ip = ip
        self.port = port
        self.clients_amount = clients_amount
        
    def create_ring(self):
        s = socket.socket()         
        s.bind((self.ip, self.port))         
        s.listen(self.clients_amount)

        clients_sockets = []
        clients_addresses = []
        
        while (len(clients_sockets) != self.clients_amount): 
            print("waiting for connections...")
            client_socket, addr = s.accept()
            client_address = client_socket.recv(1024).decode()
     
            clients_sockets.append(client_socket)
            clients_addresses.append(client_address)
            print ("Got connection from", addr)
            client_socket.send("Waiting for enough nodes to create the ring".encode()) 
        
        print("All nodes connected")
        for i in range(self.clients_amount):
            clients_sockets[i].send(str(clients_addresses[(i+1)%self.clients_amount]).encode())
            clients_sockets[i].close()
            print("Sent to", clients_addresses[i], "the address", clients_addresses[(i+1)%self.clients_amount])


if __name__ == "__main__":
    InitNode(ip, port, clients_amount).create_ring()
