import socket
import sys
import select
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Help: Specify IP Address and Port Number")
    exit()

IP_address = str(sys.argv[1])

port = int(sys.argv[2])

server.bind((IP_address, port))

server.listen(100)

client_list = []

def clientthread(conn, addr):

    conn.send("Welcome to the chat")

    while True:
        try:
            message = conn.recv(2048)
            if message:

                print("From: " + addr[0] + ": " + message)

                message_to_send = "From" + addr[0] + ": " + message
                broadcast(message_to_send, conn)

            else:
                remove(conn)

        except:
            continue

def broadcast(message, connection):
    for clients in client_list:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()

                remove(clients)

def remove(connection):
    if connection in client_list:
        client_list.remove(connection)

while True:
    conn, addr = server.accept()

    client_list.append(conn)

    print(addr[0] + "connected!")

    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()        
