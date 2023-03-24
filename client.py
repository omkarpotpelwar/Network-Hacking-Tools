import socket
import sys
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
    print("Help: Specify IP Address and Port Number")
    exit()

IP_address = str(sys.argv[1])

port = int(sys.argv[2])

server.connect((IP_address, port))

while True:
    sockets_list = [sys.stdin, server]

    read_socket, write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in sockets_list:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("Me: ")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()
