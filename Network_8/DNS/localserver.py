# Implementation of DNS Local Server

# The local server accepts connection from the client and sends the IP address of the domain name to the client.

# The local server will have its own cache in which it will store the < domain name, IP address > pairs. This cache will be used to resolve the domain names.

# If the domain name is not present in the cache, then the local server will send a query to the root server to get the IP address of the domain name.

# The root server will send the IP Address of the .com server or the .in server to the local server, according to the domain name.

# The local server will then send a query to the .com server or the .in server to get the IP address of the domain name.

# The .com server or the .in server will send the IP address of the domain name to the local server.

# The local server will then send the IP address of the domain name to the client.

# The local server will store the < domain name, IP address > pair in its cache.


# Importing the socket library and the time library
import socket
import time

IP = "127.0.0.1"
PORT = 9999

# IP address of the root server and the port number which will be used to connect to the root server 
ROOT_IP ="127.0.0.3"
ROOT_PORT=9998

# Create the cache dictionary
cache = {}

Found=False

# Dictionary of domain names with their IP addresses in format < domain name, IP address >
# google.com, 100.100.100.1
# facebook.com, 100.100.100.2
# youtube.com, 100.100.100.3 

# instagram.in, 99.99.99.1
# twitter.in, 99.99.99.2

dict_domain={}
dict_domain["google.com"]="100.100.100.1"
dict_domain["facebook.com"]="100.100.100.2"
dict_domain["youtube.com"]="100.100.100.3"
dict_domain["instagram.in"]="99.99.99.1"
dict_domain["twitter.in"]="99.99.99.2"



# Create the socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print ("Socket successfully created")
print("[ Local Server ]: Socket successfully created...")
# Bind the socket to the port
s.bind((IP, PORT))
# print ("socket binded to %s" %(PORT))
print(f"[ Local Server ]: Socket binded to {PORT}...")
# Put the socket into listening mode
s.listen(5)
# print ("socket is listening")
print("[ Local Server ]: Socket is listening...")

# Connect to the client
c, addr = s.accept()
# print ('Got connection from', addr)
print(f"[ Local Server ]: Got connection from {addr}...")
# Receive the domain name from the client
domain_name = c.recv(1024).decode()
# print("The domain name is: ",domain_name)
print(f"[ Local Server ]: The domain name is: {domain_name}...")

# Check if the domain name is present in the cache
for i in cache:
    if i==domain_name:
        Found=True
        # print("The IP address is: ",cache[i])
        print(f"[ Local Server ]: The IP address is: {cache[i]}...")
        # Send the IP address to the client
        c.send(cache[i].encode())
        # Close the connection
        c.close()
        # Close the socket
        s.close()
        break


# Function to send the query to the root server 


def send_query(domain_name):
    isReal=False
    Inter_IP=""
    # The root server will send the IP Address along with a flag to the local server, the flag will be 1 if the domain name is present in the root server and 0 if the domain name is not present in the root server.
    # If the flag is 1, then the local server will send the IP address of the domain name to the client.
    # If the flag is 0, then the local server will send a query to the Inter_IP that it will receive from the root server. The Inter_IP will be the IP address of the .com server or the .in server.
    TEMP_IP ="localhost"
    TEMP_PORT=9998
    while isReal==True:
        # Connect to the root server
        s.connect((TEMP_IP,TEMP_PORT))
        # Send the domain name to the root server
        s.send(domain_name.encode())
        # Receive the IP address and the flag from the root server
        Inter_IP=s.recv(1024).decode()
        # Received format: < IP address, port , flag >
        
        # Split the received string to get the IP address and the flag
        
        # Get the IP address
        TEMP_IP=Inter_IP.split(",")[0]
        # Get the port number
        TEMP_PORT=Inter_IP.split(",")[1]
        # Get the flag
        
        Real=Inter_IP.split(",")[2]
        isReal=int(Real)
    # Search in the dictionary of domain names and IP addresses
    for i in dict_domain:
        if i==domain_name:
            # print("The IP address is: ",dict_domain[i])
            print(f"[ Local Server ]: The IP address is: {dict_domain[i]}...")
            # Send the IP address to the client
            TEMP_IP=dict_domain[i]
            print("[ Local Server ]: IP address sent to the client...")
            # Close the connection

            # Close the socket

            break
    # Now the IP address of the domain name is present in the ROOT_IP and the ROOT_PORT
    # Now send the IP address of the domain name to the client
    # c.send(TEMP_IP.encode())
    
    # Check if the domain is .com or .in
    
    # If the domain is .com, then send the query to the .com server
    # if domain_name.split(".")[1]=="com":
    #     TEMP_IP="192.00.00.00"
    # Close the connection
    
    # Close the socket
    
    # Store the < domain name, IP address > pair in the cache
    cache[domain_name]=TEMP_IP
    
    return TEMP_IP

    



IP_Address=""

if Found==False:
    IP_Address=send_query(domain_name)
    if IP_Address!="":
        # Store the < domain name, IP address > pair in the cache
        cache[domain_name]=IP_Address
        # Send the IP address to the client
        c.send(IP_Address.encode())
        # Close the connection
        c.close()
        # Close the socket
        s.close()
    





