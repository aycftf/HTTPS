#!/usr/bin/env python3
#TODO: MAKE ENV VARS REGARDING EACH PEM FILE (key + certificate / csr)
#TO USE, SIMPLY CREATE A CERT AND KEY (e.g. openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes -keyout MyRootCA.key -out MyRootCA.crt -subj "/C=US/ST=State/L=City/O=Organization/CN=My Custom Root CA")
# THEN POINT EACH PEM FILE TO THEIR RESPECTIVE LOCATION IN "pemCrt" & "pemKey"

import ssl, sys, os
import http.server
import socket 
import subprocess as sub
import hashlib
import argparse
import zipfile

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
		except Exception as eee:
			sys.exit(f"{eee}")


# Read the file in chunks of 8192 bytes
#Hashobject using sha256
#Update hashFunc with new chunk of data

def fileServ(cSocket, file_path, file_name):
	path = file_path
	hashFunc = hashlib.new("sha256")
	with open(path, 'rb') as hashFile:
		while chunk := hashFile.read(8192):
			hashFunc.update(chunk)
		
	hashOfFile = hashFunc.hexdigest()
	print("\n [*] Current Hash of File: %s"% (hashOfFile))
	print("Reading File From: %s"% (path))
	if not os.path.isfile(path):
		pass
		try:

			with open(path, 'w+') as testFile:

				testFile.write("This is a test file to host on https server!!")



		except IOError as io:
			sys.exit(f"IO Error: {io}")

	
	else:
		print("File Already Exists..... Continuing")



	if args.file or args.dir:
		with open(path, 'rb') as fF:
			#Read data to send thru socket
			fileContent = fF.read()
			fileName = file_name
			contentType = "application/octet-stream" if args.file else "application/zip"
			print("FILE BEING SERVED TO SERVER: %s "% (fileName))

			
			##Use hashlib from python modules to produce basic hash of file
			##In future other then PoC use a dedicated file to create hash and then check
			sha256Hashh = hashlib.sha256(fileContent).hexdigest()


			if sha256Hashh == hashOfFile:

				print("[*]INFO: Hashes Match!!")



			else:
				print(f"\n File does NOT match hash!!!! ")
				sys.exit()
		

			# \r == 'carriage return'
			#\r\n == carriage return newline, return cursor to beginning and move down w/  newline
			##NOTE: ALL \R\N are included after entires, \r\n\r\n at last entry...
			resp = (

				f"HTTP/1.1 200 OK\r\n"
				f"Content-Type: {contentType}\r\n"
				f"Content-Disposition: attachment; filename={fileName}\r\n"
				f"Content-Length: {len(fileContent)}\r\n"
				f"Last-Modified: 04 Jan 2026 4:14AM EST\r\n"
				#End header content and start body
				f"\r\n"
			)

		try:
			cSocket.sendall(resp.encode('utf-8'))
			#Send all file content or chunks at once
			cSocket.sendall(fileContent)
		except socket.error as seF:
			response = "HTTP/1.1 500 Internal Server Error"
			cSocket.sendall(response.encode('utf-8'))


		






def sslServ(file_path, file_name):
	##LOCAL IP address from lIP function 
	xX = (lIP())
	xXX = xX[0]
	#print(xXX)
	##Hardcoded SSL cert, and pem to confirm client tls
	#TODO: MAKE ENV VARS REGARDING EACH PEM FILE (key + certificate / csr)
	pemCrt = "/path/to/your/certs.pem"
	pemKey = "/path/to/your/key.pem"


	#Setup ssl context and load pem key and crt
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(certfile=pemCrt, keyfile=pemKey)



	#attempt to bind socket to listen for https

	try:

		#SOCK_DGRAM = UDP, SOCK_STREAM = TCP, for tls/https
		bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#Allow the re-use of sockets to bound local IP and PORT, when dealing with TIME_WAIT or quick restarts server/client side
		bind.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		bind.bind((xXX, 4433))
		bind.listen(6)


		#wrap, enable server side tls
		sslSock = context.wrap_socket(bind, server_side=True)
		print(f"\n [*] Python https server running on port 4433 on localhost %s"% (xXX))



		while True:
			try:
				
				#always listen and accept sockets, and get peer connection content
				cSocket, ip = sslSock.accept()
				getSockName = cSocket.getpeername()


				#recv 1024 bytes of data at a time and decode to readable text
				dataClient = cSocket.recv(1024).decode('utf-8')
				print("[*] Connection from Client Recieved..... \n")
				print("[*] Data about connection:")
				print(dataClient)

				#if length of our REQ / GET is greater then 0

				if len(dataClient.splitlines()) > 0:
				
					#test = "Hello!"
					#testt = test.encode()
					print("SSL connection successful from: " + ip[0])

					fileServ(cSocket, file_path, file_name)
					
					cSocket.close()
				else:
					cSocket.close()
					sys.exit("Faulty Request....")
			except socket.error as sEE:
				if "http request" in str(sEE):
					import time
					print(f"\n GOT HTTP REQUEST ON HTTPS SERVER... COULD NOT ESTABLISH")
					time.sleep(2)
					


				elif "bad length" in str(sEE):
					print("Download cancled from client before data could be properly parsed, and downloaded....")
	

				elif "certificate unknown" in str(sEE):
					print("Certificate not recognized, possibly need to allow 'insecure' request to allow tls connection within browser....")
					print("\nKeeping Connection Alive and Waiting... ")

			

				else:
					print(f"{sEE}")
					sys.exit("EXITING NOW!!")






	except Exception as fE:
		sys.exit(f"EXCEPTION CAUGHT: {fE}")

	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Simple HTTPS server')
	parser.add_argument('-f', '--file', help='File to serve')
	parser.add_argument('-d', '--dir', help='Directory to serve')
	args = parser.parse_args()
	##Handle dir and files w/ args specified
	if args.dir:
		dir_path = os.path.join(os.getcwd(), args.dir)
		#Check if user supplied input is infact a dir
		if not os.path.isdir(dir_path):
			print(f"Directory {dir_path} does not exist.")
			sys.exit(1)
		zip_name = args.dir + '.zip'
		##Tack on zip extension to dir name
		zip_path = os.path.join(os.getcwd(), zip_name)
		if not os.path.exists(zip_name):
			print(f"Creating zip file {zip_name} from directory {dir_path}...")
			#Create zip file from directory (w/ zipfile lib), and update function parameters to serve
			#Use ZIP_DEFLATED to compress zip file, and allowZip64 for large files
			with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
				#Walk thru all files in origional directory and add to zip
				for root, dirs, files in os.walk(dir_path):
					for file in files:
						#Join & Write root path of files in directory (from loop), and add to zip with relative path of cwd files are located in (avoid abspath in zip)
						#TLDR: Keep directory structure adjacent with reg directory
						zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dir_path))
			#Update args
			path = zip_path
			print("[*] ZIP PATH %s"% (path))
			file_name = zip_name
		else:
			print(f"Zip file {zip_name} exists, serving as normal from {zip_path}...")
			path = zip_path
			print("[*] ZIP PATH %s"% (path))
			file_name = zip_name
	elif args.file:
		path = os.path.join(os.getcwd(), args.file)
		file_name = args.file
	else:
		print("Specify -f file or -d dir")
		sys.exit(1)
	ipad = lIP()
	if ipad:
		print(f"[*] Local IP: {ipad[0]}")
		print("[*] Stop HTTPS server anytime with Ctrl+C")
		sslServ(path, file_name)





