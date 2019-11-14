from __future__ import print_function
from socket import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import md5
import random
import os
import io
from termcolor import cprint
import time


def encrypt(message,cipher):
	padded = message + " "*(16-len(message)%16)
	ciphertext = cipher.encrypt(padded)
	return ciphertext
	
def decrypt(message,cipher):
	text = cipher.decrypt(message)
	text = text.strip()
	return text

P=1000000000000241
g=23
b=17
y=pow(g,b)%P

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("",serverPort))
serverSocket.listen(1)
print("The server is ready to receive connections")
while True:
	connectionSocket, addr = serverSocket.accept()
	connfd=connectionSocket.fileno()

	#RSA Authentication
	cprint("RSA Authentication :","white","on_cyan")
	print()
	rsa_string=connectionSocket.recv(1024)
	rsa_string=rsa_string.strip()
	rsa_public_key=RSA.importKey(rsa_string)
	rand_val = str(random.randint(0,10000))
	encrypted = rsa_public_key.encrypt(rand_val, 32)
	connectionSocket.send(encrypted[0])
	clientmd5=connectionSocket.recv(1024)
	servermd5=md5.new(rand_val).digest()
	if(clientmd5==servermd5):
		cprint("Client Successfully Authenticated","white","on_green")
		connectionSocket.send("Authentification Successful")
	else:
		cprint("Client Authentication Failed","white","on_red")
		connectionSocket.send("Error:Authentification Failed")
		continue
	
	cprint("\nCommunication in Plain Text :","white","on_cyan")
	print()
	message = "Server:Hello Client"
	rmessage=connectionSocket.recv(1024)
	print("Recieved :",rmessage)
	connectionSocket.send(message)
	print("Sent :",message)
	rmessage=connectionSocket.recv(2)

	#Diffie-Hellman Algorithm for Key Sharing
	cprint("\nDiffie-Hellman Key Exchange :","white","on_cyan")
	print()
	x=connectionSocket.recv(1024)
	x=int(x)
	print( "Recieved :", x)
	prkey=pow(x,b)%P
	prkey=str(prkey)
	connectionSocket.send(str(y))
	print("Sent :",y)
	cprint("Server - Shared Private Key = " + prkey ,"green")
	md5key = md5.new(prkey).digest() #AES needs 16-byte Key. MD5 hashes the generated key "prkey" to a 16-byte string.
	cipher = AES.new(md5key, AES.MODE_CBC,'This is an IV456')

	cprint("\nCommunication with AES Encryption :","white","on_cyan")
	print()
	message = "Server:Hello Client"
	rmessage=connectionSocket.recv(1024)
	print("Recieved :",decrypt(rmessage,cipher))
	connectionSocket.send(encrypt(message,cipher))
	print("Sent :",message)
	rmessage=connectionSocket.recv(2)
	print("\n---------------------------------------------------------\n")
	while(True):
		dir = "\n~" + os.getcwd() + "/ "
		connectionSocket.send(encrypt(dir,cipher))
		cmd=connectionSocket.recv(2048)
		cmd=decrypt(cmd,cipher)
		if(cmd.split()[0]=="cd"):
			direct = cmd.split()[1]
			if(os.path.isdir(direct)):
				os.chdir(direct)
				string = "Directory Changed"
			else:
				string = "No such Directory"
			connectionSocket.send(encrypt(string,cipher))
			time.sleep(0.5)
			continue

		cmd2=""
		cmd1=cmd
		#if("|" in cmd):
			#cmd1,cmd2=cmd.split('|')
		cmd1=cmd1.split()
		cmd2=cmd2.split()
		if(len(cmd2)==0):
			pid = os.fork()
			if(pid==0):
				f=open("temp.txt","w")
				os.dup2(f.fileno(),1)
				os.execvp(cmd1[0],cmd1)
				f.close()
				break
			elif(pid!=-1):
				os.wait()
				f=open("temp.txt","r")
				string = str(f.read())
				connectionSocket.send(encrypt(string,cipher))
				f.close()
		else:
			print(2)
			pid=os.fork()
			if(pid==0):
				cpid=os.fork()
				inp,out=os.pipe()
				if(cpid==0):
					os.close(inp)
					os.dup2(out,1)
					os.execvp(cmd1[0],cmd1)
				elif(cpid!=-1):
					os.wait()
					os.close(out)
					f=open("temp.txt","w")
					os.dup2(inp,0)
					os.dup2(f.fileno(),1)
					os.execvp(cmd2[0],cmd2)
					f.close()
				break
			elif(pid!=-1):
				os.wait()
				f=open("temp.txt","r")
				string = str(f.read())
				connectionSocket.send(encrypt(string,cipher))
				f.close()
			
		
			
					

	

	connectionSocket.close()
