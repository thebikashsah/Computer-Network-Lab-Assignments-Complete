# Implementation of DNS client

# Client will have its own local cache in which it will store the 
# < domain name, IP address > pairs. This cache will be used to 
# resolve the domain names. 
# If the domain name is not present in the cache, then the client will send a query to the local server.

# When the client receives the response from the server, it will store the < domain name, IP address > pair in its cache. 


# The client will only contact the local server. It will not contact any other server.


# Importing the socket library and the time library
import socket
import time

# Store the IP address of the local server and the port number
IP="localhost"
PORT=9999

# Create the cache dictionary
cache={}
# Create the socket object
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Take the domain name as input from the user
domain_name=input("Enter the domain name: ")

# Check if the domain name is present in the cache

isFound=False
for i in cache:
    if i==domain_name:
        isFound=True
        print("The IP address is: ",cache[i])
        break

IP_ADDRESS=""

# Function to send the query to the server
def send_query(domain_name):
    # Connect to the server
    s.connect((IP,PORT))
    # Send the domain name to the server
    s.send(domain_name.encode())
    # Receive the IP address from the server
    IP_ADDRESS=s.recv(1024).decode()
    # Close the connection
    # s.close()
    # Return the IP address
    return IP_ADDRESS

if not isFound:
    # If the domain is not found call a function to send the query to the server
    IP_ADDRESS=send_query(domain_name)
    
    # If the IP address is not empty, then store the < domain name, IP address > pair in the cache
    
    if IP_ADDRESS!="":
        cache[domain_name]=IP_ADDRESS
        print("The IP address is::",IP_ADDRESS)
    else:
        print("The domain name is not present in the DNS server")
        
