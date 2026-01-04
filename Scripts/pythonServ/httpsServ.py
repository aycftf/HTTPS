#!/usr/bin/env python3


import ssl, sys, os
import http.server
import socket 
import subprocess as sub
import hashlib

def lIP():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		lip = s.getsockname()
		s.close()
		return lip

	except socket.error as se:
		try:
			lip = socket.gethostbyname(socket.gethostname())
			if lip.startswith("127.") or lip.startswith("192.254"):
				return "Could not get local ip"
			else:
				return lip[0]
		except Error as eee:
			sys.exit(f"{eee}")




def fileServ(cSocket):

	HASHH = "677c4d57aa034dc192b5191870141057574c1b05df2b9569c0ee08aa4e32125d"
	dir = os.getcwd()
	path = f"{dir}/debian-13.2.0-amd64-netinst.iso"
	print(path)
	if not os.path.isfile(path):
		pass
		try:

			with open(path, 'w+') as testFile:

				testFile.write("This is a test file to host on https server!!")



		except IO.error as io:
			sys.exit(f"IO Error: {io}")

	
	else:
		print("File Already Exists..... Continuing")




	with open(path, 'rb') as fF:
		fileContent = fF.read()
		fileName = os.path.basename(path)
		print("FILE BEING SERVED TO SERVER: %s "% (fileName))

		
		##Use hashlib from python modules to produce basic hash of file
		sha256Hashh = hashlib.sha256(fileContent).hexdigest()


		if sha256Hashh == HASHH:

			print("[*]INFO: Hashes Match!!")



		else:
			print(f"\n File does NOT match hash!!!! ")
			sys.exit()
	





		# \r == 'carriage return'
		#\r\n == carriage return newline, return cursor to beginning and move down w/  newline
		##NOTE: ALL \R\N are included after entires, \r\n\r\n at last entry...
		resp = (

			f"HTTP/1.1 200 OK\r\n"
			f"Content-Type: application/octet-stream\r\n"
			f"Content-Disposition: attatchment; filename={fileName}\r\n"
			f"Content-Length: {len(fileContent)}\r\n"
			f"Last-Modified: 04 Jan 2026 4:14AM EST\r\n\r\n"
			f"\r\n"




		)

	try:
		cSocket.sendall(resp.encode('utf-8'))
		cSocket.sendall(fileContent)
	except socket.error as seF:
		response = "HTTP/1.1 500 Internal Server Error"
		cSocket.sendall(response.encode('utf-8'))







def sslServ():
	xX = (lIP())
	xXX = xX[0]
	#print(xXX)
	pemCrt = "/home/useruser/Downloads/Scripts/certs/clientfiles/selfcrt.pem"
	pemKey = "/home/useruser/Downloads/Scripts/certs/clientfiles/self.pem"
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(certfile=pemCrt, keyfile=pemKey)



	#attempt to bind socket to listen for https

	try:

		#SOCK_DGRAM = UDP, SOCK_STREAM = TCP, for tls/https
		bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		bind.bind((xXX, 4433))
		bind.listen(6)


		#wrap
		sslSock = context.wrap_socket(bind, server_side=True)
		print(f"\n [*] Python https server running on port 4433 on localhost %s"% (xXX))



		while True:

			cSocket, ip = sslSock.accept()
			getSockName = cSocket.getpeername()

			dataClient = cSocket.recv(1024).decode('utf-8')
			print(dataClient)

			#if length of our REQ / GET is greater then 0

			if len(dataClient.splitlines()) > 0:
			
				test = "Hello!"
				testt = test.encode()
				print("SSL connection successful from: " + ip[0])

				fileServ(cSocket)
				
				cSocket.close()
			else:
				sys.exit("Faulty Request....")



	except socket.error as sEE:
		if "http request" in str(sEE):
			print(f"\n GOT HTTP REQUEST ON HTTPS SERVER... COULD NOT ESTABLISH")


		elif "bad length" in str(sEE):
			print("Download cancled from client before data could be properly parsed, and installed....")
			

		else:
			print(f"{sEE}")
			sys.exit("EXITING NOW!!")


	except Exception as fE:
		sys.exit(f"EXCEPTION CAUGHT: {fE}")

	


if __name__ == "__main__":
	ipad = (lIP())
	ipp = "192.168.12.127"
	#ssLFunc = sslServ(lIP)
	if ipad:
		print(f"Local IP: {ipad[0]}")
		while True:
			if sslServ():
				comm = "clear"
				runCom = sub.run(comm, text=True, check=True)
				print(runCom.stdout)





