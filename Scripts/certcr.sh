#!/usr/bin/env bash

cdd=$(pwd)
rooty=$(echo "$UID")
curuser=$(id | cut -d ' ' -f 1)
#check root
if ! [ "$rooty" = 0 ]; then
	echo -e " Please run as root... currently running as $curuser \n" && exit 1


fi


CERTDIR="$cdd/certs"
certfunc() {



	mkdir -p "$CERTDIR"
	mkdir "$CERTDIR/crl"
	mkdir "$CERTDIR/newcerts" 
	touch "$CERTDIR/index.txt"
	echo "1000" > "$CERTDIR/serial"
	scp /usr/lib/ssl/openssl.cnf "$CERTDIR/openssl.cnf"
	echo -e "\n" 
	echo -e "if issues persist with CA / cert policy, check both system clock is updated and in sync (hw and software clock)... and maybe change  policy_match to policy_anything in openssl.cnf...."


	read -p "Password protect CA file? (y/n): " -en 1 passproct
	if [[ "$passproct" =~ y|Y ]]; then
		echo -e "[*] Saving ca Key File to ca.key "
		echo -e "[*] Saving ca Cert File to ca.crt "
		echo -e "[*] Using config from /usr/lib/ssl/openssl.cnf "
		echo -e "[*] Saving to $CERTDIR Directory.. "
		# Create CA.crt and CA.key for crt: openssl req -new -x509 -keyout ca.key -out ca.crt -config openssl.cnf
		#Create client/crt key and csr: openssl genrsa -verbose -out ""${pwdd}/customerkey.key" 2048
		# Create CSR:   openssl req -new -key customerkey.key -out mycertreq.csr -config openssl.cnf
		#Create Final CRT for client: openssl ca -in mycertreq.csr -out clientCRT.crt -cert ca.crt -keyfile ca.key -config openssl.cnf



		#Convert key file to .pem: openssl rsa -in yourkey.key -out yourkey.pem -outform PEM
		#Convert crt file to .pem: openssl x509 -inform PEM -in server.crt > public.pem ORRRR  openssl x509 -inform DER -outform PEM -in server.crt -out server.crt.pem
		#Both in one pem file: cat server.crt server.key > server.includesprivatekey.pem

	fi	

}




read -p " $cdd directory okay for creating dedicated cr and ca keys? (y/n): " -en 1 keydir
if [[ "$keydir" =~ y|Y ]]; then
	certfunc


fi
