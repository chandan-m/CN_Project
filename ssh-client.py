from __future__ import print_function
from socket import *
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import AES
import md5
from termcolor import cprint
import sys


def encrypt(message,cipher):
	padded = message + " "*(16-len(message)%16)
	ciphertext = cipher.encrypt(padded)
	return ciphertext
	
def decrypt(message,cipher):
	text = cipher.decrypt(message)
	text = text.strip()
	return text

random_generator = Random.new().read
rsa_private_key = RSA.generate(1024, random_generator)
rsa_public_key = rsa_private_key.publickey()

P=1000000000000241
g=23
a=11

serverName = '192.168.24.145'
if len(sys.argv)>1:
	serverName = sys.argv[1]

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
#
#clientSocket.send(sentence)
#var = clientSocket.recv(1024)

#RSA Authentication
cprint("RSA Authentication :","white","on_cyan")
print()
clientSocket.send(rsa_public_key.exportKey())
encrypted = clientSocket.recv(1024)
decrypted = rsa_private_key.decrypt(encrypted)
clientmd5 = md5.new(decrypted).digest()
clientSocket.send(clientmd5)
result = clientSocket.recv(1024)

if "Error" in result:
	cprint(result,"white","on_red")
	exit(0)
else:
	cprint(result,"white","on_green")

#Communication in Plain Text
cprint("\nCommunication in Plain Text :","white","on_cyan")
print()
message = "Client:Hello Server"
clientSocket.send(message)
print("Sent :",message)
rmessage=clientSocket.recv(1024)
clientSocket.send("OK")
print("Recieved :",rmessage,"\n")

#Diffie-Hellman Algorithm for Key Sharing
cprint("\nDiffie-Hellman Key Exchange :","white","on_cyan")
print()
x=pow(g,a)%P
clientSocket.send(str(x))
print("Sent :",x)
y=clientSocket.recv(1024)
y=int(y)
print("Recieved :",y)
prkey=pow(y,a)%P
prkey=str(prkey)
cprint("Client - Shared Private Key =" + prkey,"green")
md5key = md5.new(prkey).digest() #AES needs 16-byte Key. MD5 hashes the generated key "prkey" to a 16-byte string.
cipher = AES.new(md5key, AES.MODE_CBC,'This is an IV456')

cprint("\nCommunication with AES Encryption :","white","on_cyan")
print()
message = "Client:Hello Server"
clientSocket.send(encrypt(message,cipher))
print("Sent :",message)
rmessage=clientSocket.recv(1024)
clientSocket.send("OK")
print("Recieved :",decrypt(rmessage,cipher))
print("\n---------------------------------------------------------\n")
rmessage=clientSocket.recv(2048)
cprint(decrypt(rmessage,cipher),"cyan",end ="")
print("$",end=" ")
cmd = raw_input()
while(cmd.upper()!="QUIT"):
	clientSocket.send(encrypt(cmd,cipher))
	l=clientSocket.recv(1024)
	data=l
	while(len(l)==1024):
		l=clientSocket.recv(1024)
		data+=l
	rmessage=decrypt(data,cipher)
	print(rmessage)
	rmessage=clientSocket.recv(2048)
	cprint(decrypt(rmessage,cipher),"cyan",end ="")
	print("$",end=" ")
	cmd = raw_input()












#
clientSocket.close()