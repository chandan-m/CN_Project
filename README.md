CN Project
SSH - Client using Sockets

The SSH protocol (also referred to as Secure Shell) is a method for secure remote login from one computer to another. It provides 
several alternative options for strong authentication, and it protects the communications security and integrity with strong encryption.
It is a secure alternative to the non-protected login protocols (such as telnet, rlogin) and insecure file transfer methods (such as FTP).
In this project we have implemented the functionalities of the SSH protocol. An abstract of our implementation is provided below – 

The most important feature of the SSH protocol is the secure connection between the client and the server. We have established this 
through the RSA authentication mechanism where the client generates a Public Key and Private Key Pair from a generated random number
using RSA module. This public key is sent to the server through a socket, using which it encrypts a random message and sends the encrypted
message back the client. The client then confirms its authenticity by sending the MD5 hash of the received message which server verifies
and the connection is established.
A comparison is provided between a plain text and an encrypted communication over the authenticated channel. The secure message 
passing/communication between the client and server is provided using the AES encryption which uses the Diffie-Hellman Algorithm for 
key exchange. Implementation of the AES encryption requires the key to be of 16 bytes which was achieved by converting the key to its
MD5 equivalent.

The shell is implemented using the fork() and exec() system calls on the server. All socket communication between the client and the 
server is AES encrypted and hence secure!

Requirements:
Python 2.7x
pip install pycrypto
pip install rsa
pip install termcolor

Execution Steps:

Client:
python ssh-client.py <IP-ADDRESS of SERVER>

Server: 
python ssh-server.py
