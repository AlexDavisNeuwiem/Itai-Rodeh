import socket     

ip = "127.0.0.1"
port = 12345
N = 3
K = 2


class InitNode:
    
    def __init__(self, ip, port, n, k):
        self.ip = ip
        self.port = port
        self.n = n
        self.k = k
        
    def create_ring(self):
        s = socket.socket()         
        s.bind((self.ip, self.port))         
        s.listen(self.n)

        clients_sockets = []
        clients_addresses = []
        
        while len(clients_sockets) != self.n:
            print("waiting for connections...")
            client_socket, addr = s.accept()
            client_address = client_socket.recv(1024).decode()
     
            clients_sockets.append(client_socket)
            clients_addresses.append(client_address)
            print("Got connection from", addr)
            client_socket.send(str((self.n, self.k)).encode())
        print("All nodes connected")
        for i in range(self.n):
            msg = str((clients_addresses, (i+1) % self.n))
            clients_sockets[i].send(msg.encode())
            clients_sockets[i].close()
            print("Sent to", clients_addresses[i], "the address", clients_addresses[(i+1) % self.n])


if __name__ == "__main__":
    InitNode(ip, port, N, K).create_ring()
