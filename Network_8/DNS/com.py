# Implemenation of DNS .com Server
# It will store the < domain name, IP address > pairs in the cache.
# It will accept connection from the local server and send the IP address of the domain name to the local server.


import socket


IP_COM="127.0.0.1"
PORT_COM=9997

# Create the cache dictionary
cache={}
cache["google.com"]="199.99.99.99"
cache["facebook.com"]="200.200.200.200"

# Create the socket object
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Bind the socket to the port
s.bind((IP_COM,PORT_COM))

# Put the socket into listening mode
s.listen(5)
print("[ .com Server ]: Socket is listening...")

# Connect to the local server
c,addr=s.accept()
print(f"[ .com Server ]: Got connection from {addr}...")
# Receive the domain name from the local server
domain_name=c.recv(1024).decode()
print(f"[ .com Server ]: The domain name is: {domain_name}...")

# Send the IP address of the domain name to the local server

# Send in the format < IP address port number 1 >
c.send((cache[domain_name]+" "+str(PORT_COM)+" 1").encode())
print(f"[ .com Server ]: The IP address is: {cache[domain_name]}...")

# Close the connection
c.close()
# Close the socket
s.close()


