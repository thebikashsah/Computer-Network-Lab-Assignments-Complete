import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 9999
my_IP = input("[ CLIENT ] Enter the IP for this Client: ")
my_Mac = input("[ CLIENT ] Enter the MAC for this Client: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)
username = my_IP.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
while True:

    ip_receiver = input("[ CLIENT ] Enter the IP of Receiver: ")
    

    # this is for ARP request

    if ip_receiver:
        message = my_IP + " " + my_Mac + " " + ip_receiver + " " + "FF.FF.FF.FF.FF.FF"
        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:
            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)
            # If we received no data, server gracefully closed a connection, for example using socket.close() or
            # socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print("[ CLIENT ] Connection closed by the Server...")
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')
            # Now do the same for message (as we received username, we received whole message, there's no need to
            # check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            ARP_request = message.split()
            if ARP_request[2] == my_IP:
                ARP_reply = my_IP + " " + my_Mac + " " + ARP_request[0] + " " + ARP_request[1]
                ARP_reply = ARP_reply.encode('utf-8')
                ARQ_header = f"{len(ARP_reply):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(ARQ_header + ARP_reply)
            else:
                print("----------------------------------------")
                print("[ CLIENT ] Discarded the Request...")
                print("----------------------------------------")
            # Print message
            print(f'{username} > {message}')
    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('[ CLIENT ] Reading Error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print(' [ CLIENT ] Reading Error: '.format(str(e)))
        sys.exit()
