from socket import *
import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

# Konfigurasi logging untuk menyimpan output ke file
logging.basicConfig(filename='lb_process.log', level=logging.WARNING,
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class BackendList:
    def __init__(self):
        self.servers = [
            ('127.0.0.1', 9000),
            ('127.0.0.1', 9001),
            ('127.0.0.1', 9002)
        ]
        self.current = 0

    def getserver(self):
        s = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return s

def ProcessTheClient(connection, backend_sock, mode='toupstream'):
    try:
        while True:
            if mode == 'toupstream':
                datafrom_client = connection.recv(1024)
                if datafrom_client:
                    backend_sock.sendall(datafrom_client)
                else:
                    backend_sock.close()
                    break
            elif mode == 'toclient':
                datafrom_backend = backend_sock.recv(1024)
                if datafrom_backend:
                    connection.sendall(datafrom_backend)
                else:
                    connection.close()
                    break
    except Exception as e:
        logging.warning(f"Error: {str(e)}")
    finally:
        connection.close()

def Server():
    my_socket = socket(AF_INET, SOCK_STREAM)
    my_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    backend = BackendList()

    my_socket.bind(('0.0.0.0', 44444))
    my_socket.listen(5)
    logging.warning("Load balancer running on port 44444")

    with ProcessPoolExecutor(20) as executor:
        while True:
            connection, client_address = my_socket.accept()
            backend_sock = socket(AF_INET, SOCK_STREAM)
            backend_sock.settimeout(1)
            backend_address = backend.getserver()
            logging.warning(f"{client_address} connecting to {backend_address}")

            try:
                backend_sock.connect(backend_address)
                executor.submit(ProcessTheClient, connection, backend_sock, 'toupstream')
                executor.submit(ProcessTheClient, connection, backend_sock, 'toclient')
            except Exception as err:
                logging.error(err)
                connection.close()

def main():
    Server()

if __name__ == "__main__":
    main()

