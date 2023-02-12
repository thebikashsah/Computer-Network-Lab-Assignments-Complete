# Implementation of DNS Root Server 

# The root server accepts connection from the local server and sends the IP address of the .com server or the .in server to the local server, according to the domain name.

import socket

# IP address of the root server and the port number which will be used to connect to the root server

ROOT_IP ="127.0.0.1"
ROOT_PORT=9998


IP_COM="127.0.0.4"
PORT_COM=9997

IP_IN="10.10.10.4"
PORT_IN=9996



# It will receive the domain name from the local server and send the IP address of the .com server or the .in server to the local server, according to the domain name.

# Socket object
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Bind the socket to the port
s.bind((ROOT_IP,ROOT_PORT))

# Put the socket into listening mode
s.listen(5)
print("[ Root Server ]: Socket is listening...")

# Connect to the local server
c,addr=s.accept()

# Receive the domain name from the local server
domain_name=c.recv(1024).decode()

print(f"[ Root Server ]: The domain name is: {domain_name}...")
# Extract the extension of the domain name 
extension=domain_name.split(".")[-1]



# Send the IP address of the .com server or the .in server to the local server, according to the domain name.
# It will send in the format < IP address port number 0 >
if extension=="com":
    print(f"[ Root Server ]: Sending IP address of .com server to the local server...")
    c.send((IP_COM+" "+str(PORT_COM)+" 0").encode())
elif extension=="in":
    print(f"[ Root Server ]: Sending IP address of .in server to the local server...")
    c.send((IP_IN+" "+str(PORT_IN)+" 0").encode())
    
# Close the connection
c.close()
# Close the socket
s.close()

# Write in the file pychache.txt the IP address of the .com server and the .in server
