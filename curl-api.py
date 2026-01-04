#!/usr/bin/env bash

##test api token valididty



##Open AI search query to use:

import httpx, sys, time, os
import subprocess as sub
import httpx


KEYS= [""]
URL = "https://api.openai.com/v1/models"



'''
for token in KEYS:

	resp = {}
	token.split()
 

	#Add headers to test response with apikeys
	headers = {

		"Authorization": f'Bearer {token}',
		"Accept": "application/json"

	}

	try:
		response = httpx.get(URL, headers=headers)

		resp[token] = response.json()
		#print(response.json())
		

		for _, v in resp.items():
			for vitems in v.values():
				#print(vitems)

				checkKey = vitems['message'][:18]

				if 'incorrect' in str(checkKey).lower():
					print("\nINCORRECT KEY\n")
					print(f"\nAttempted Key: {token}\n")


	except Exception as e:
		sys.exit(f"Error in http response.. : \n {e}")

'''

def addKeys():
	dumpuri = "http://127.0.0.1:8080/apilist"
	getDump = "curl -fsS http://127.0.0.1:8080/apilist -O && mv apilist Dump.txt >> /dev/null"
	readKeysComm = "cat Dump.txt"
	checkStat = httpx.get(dumpuri)
	entryKeys = []
	DumpPath="/home/whftf/Downloads/Scripts/HTTPSTUFF/Dump.txt"
	if checkStat.status_code == 200:

		try:
			
			dumpFilesComm = sub.run(getDump, shell=True, check=True, capture_output=True, text=True)
			readKeys = sub.run(readKeysComm, shell=True, capture_output=True, text=True)
			print(f" GRABBED KEYS FROM SCRAPE: ")
			print(" --------------------------- ")


			lenofKey = len(readKeys.stdout)
			
			if os.path.exists(DumpPath):
				print("\n Parsing Dumpfile. \n")


				#Read bytes from curl output
				with open(DumpPath, "rb") as rdK:
					readDump = rdK.read()
					#Decode bytes to utf-8
					dumpDecode = readDump.decode('utf-8')
					#Strip every entry in file loop, as well as splitting lines from decoded bytes
					entryLoop = [entry.strip() for entry in dumpDecode.splitlines() if entry.strip()]

					t = 1
					for en in entryLoop: 
						entryKeys.append(en)
						print(f"Parsed Key {t}/{len(entryLoop)} : \n {en} \n")
						t += 1
						time.sleep(0.05)


		except Exception as e:
			sys.exit(f"{e}")




		os.remove(DumpPath)


	return entryKeys

				



			
#if x.endswith("None"):
#	print(f"{x} has None")
#	changeNone = x[:-4]
#	print(changeNone, end='')


#else:
#	print(x, end='')

	


###For OPEN_AI KEYS
def TestKeys(Dump):
	###Test infinite loop for rate limit
	while True:

		try:
			for k in Dump:
				k.split()
				#Add headers to test response with apikeys
				headers = {

				"Authorization": f'Bearer {k}',
				"Accept": "application/json"

				}

				data = {



				}

				response = httpx.get(URL, headers=headers, timeout=10)
				if response.status_code == 401:
					print("Unauthorized...")
					print("trying next key..")
					#print(f"\n\n {response.json()}")

					
				else:
					print("\n\n\n")
					print("API KEY FOUND!!")
					time.sleep(1)
					print(f"\n\n{response.json()}")
					break

		except httpx.HTTPStatusError as e:
			print(f"Status Error.. \n {e}")
				


'''


All HTTPX except handling:
except httpx.HTTPStatusError as e:
    print(f"HTTP Error: {e.response.status_code} for {e.request.url}")
except httpx.TimeoutException:
    print("Request timed out.")
except httpx.RequestError as e: # Catches other request-related errors
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

'''





def main():

	x = addKeys()
	y =TestKeys(x)
	if y:
		print(y)
	



if __name__ == "__main__":
	main()