import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 9999
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[ SERVER ] Starting Server...")
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
print("[ SERVER ] Server binded to IP: " + IP + " and Port: " + str(PORT))
# This makes server listen to new connections
server_socket.listen()
# List of sockets for select.select()
sockets_list = [server_socket]
# List of connected clients - socket as a key, user header and name as data
clients = {}
# for storing the ARP requesting clients
ARP_request = {}
print(f'[ SERVER ] Listening for Connections on IP : {IP} PORT : {PORT}...')


# Handles message receiving
def receive_message(client_socket):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False


while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # Iterate over notified sockets
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()
            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue
                # Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            # Also save username and username header
            clients[client_socket] = user

            print('[ SERVER ] Accepted new Connection from username IP: {}'.format(user['data'].decode('utf-8')))

            # Else existing socket is sending a message
        else:
            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('[ SERVER ] Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue
                # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'[ SERVER ] Received message from IP {user["data"].decode("utf-8")}:')


            # Iterate over connected clients and broadcast message
            # Splitting the incoming packet
            ARP_packet = message["data"].decode("utf-8").split()
            print("-----------------------PACKET ---------------------------")
            print(f"[ SERVER ] SENDER IP: {ARP_packet[0]}")
            print(f"[ SERVER ] SENDER MAC: {ARP_packet[1]}")
            print("---------------------------------------------------------")
            print(f"[ SERVER ] RECEIVER IP: {ARP_packet[2]}")
            print(f"[ SERVER ] RECEIVER MAC: {ARP_packet[3]}")
            print("---------------------------------------------------------")

            # this is ARP request
            if ARP_packet[3] == "FF.FF.FF.FF.FF.FF":
                ARP_request[ARP_packet[0]] = notified_socket
                for client_socket in clients:

                    # But don't send it to sender
                    if client_socket != notified_socket:
                        # Send user and message (both with their headers) We are reusing here message header sent by
                        # sender, and saved username header send by user when he connected
                        client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
            # else it is an ARP reply therefore it must be uni-cast.
            else:
                if ARP_packet[2] in ARP_request:
                    ARP_request[ARP_packet[2]].send(user['header'] + user['data'] + message['header'] + message['data'])

        # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]


# Design of the Server
# The server is designed to be a simple ARP server. It will receive ARP packets from the clients and will send them to the  destination client. The server will also send the ARP reply to the client who requested the ARP reply.

# Design of the Client
# The client is designed to be a simple ARP client. It will send ARP packets to the server and will receive the ARP reply from the server. The client will also send the ARP reply to the destination client.