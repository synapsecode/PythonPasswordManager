import os
import json 
from cryptography.fernet import Fernet
import sys
import argparse
from prettytable import PrettyTable

base = os.path.dirname(os.path.abspath(__file__))
config = json.loads(open(os.path.join(base, "config.json"), "rb").read() or "{}")


#Getting the CryptoKey from the Environment Variables
cryptokey = os.environ.get('ppmkey')

"""
TO ADD:
1. Support to store cryptokey in env


DONE
1. Support for Environment Variable key
"""

def ScanASCII(iterable):
	a = 0
	L = []
	for i in iterable:
		L.append(a+ord(i))
		a+=ord(i)
	return L

def ceasar_cipher(s, shift, decrypt=False):
	shift = -shift if decrypt else shift
	ccipher = ""
	for ch in s:
		if(ch.isalpha()):
			if (ch.isupper()):
				ccipher += chr((ord(ch) + shift - 65) % 26 + 65)
			else:
				ccipher += chr((ord(ch) + shift - 97) % 26 + 97)
		elif(ch.isdigit()):
			ccipher += chr((ord(ch) + shift - 48) % 10 + 48)
		else:
			#Specal Characters
			SCR = [tuple(x) for x in [range(32,47+1), range(58,64+1), range(91,96+1), range(123,126+1)]]
			z = ord(ch)
			for T in SCR:
				if(z in T):
					ccipher += chr((z + shift - T[0]) % len(T) + T[0])
					break
	return ccipher


def crypto(S, dec=False):
	# print("CRP:", S, dec)
	# cryptokey = config['authkey']
	K = config['authkey']
	F = Fernet(K)
	#Encryption or Decryption
	S = S if dec else bytes(S, encoding='ascii')
	return F.decrypt(S) if dec else F.encrypt(S)

def encrypt(s, k):
	enck = ceasar_cipher(k, len(s)) #Ceasar Encrypting key
	# asciisum = sum([ord(x) for x in enck]) #Ascii sum of Encrypted Key

	asciisum = sum(ScanASCII(enck)) #New Scanning Sun
	encs = ceasar_cipher(s, asciisum) #Ceasar Encrypting of String
	cen = crypto(encs) #Cryptographic Encoding
	return encs, cen

def decrypt(s, k):
	cdec = crypto(s, dec=True) #Cryptographic Decoding
	S = cdec.decode('ascii') #Bytes -> String
	deck = ceasar_cipher(k, len(S)) #Ceasar Encrypting key
	# asciisum = sum([ord(x) for x in deck]) #Ascii sum of Encrypted Key
	asciisum = sum(ScanASCII(deck)) #New Scanning Sun
	decs = ceasar_cipher(S, asciisum, decrypt=True) #Ceasar Decrypting of String
	return decs

if __name__ == '__main__':
	#Arguement Parser Stuff
	parser = argparse.ArgumentParser()
	parser.add_argument('command', help="PPM Command", type= str)
	parser.add_argument('--cryptokey', '-k', help="Cryptographic Key", type= str)
	parser.add_argument('--object', '-o', help="Payload Object", type= str)
	parser.add_argument('--name', '-n', help="Password Field Name", type= str)
	parser.add_argument('--password', '-p', help="Password", type= str)
	parser.add_argument('--ppxpath', '-ppxp', help="PPXPath", type= str)
	args = parser.parse_args()

	def check_cryptokey():
		global cryptokey
		if(args.cryptokey):
			cryptokey = args.cryptokey

		if(not args.cryptokey and not cryptokey):
			print("Please Include the Global CryptoKey with the -k flag or add it to your Environment Variables as 'ppmkey'")
			exit()

	def get_enc_path(p):
		return base if p == "base" else p

	def save_enc():
		with open(os.path.join(get_enc_path(config['ppxpath']), "encdata.ppx"), "w") as f:
			f.write(json.dumps(D))

	def save_config():
		with open(os.path.join(base, "config.json"), "w") as f:
				f.write(json.dumps(config))
	
	#?Create .ppx file if doesnt exist
	D = json.loads(open(os.path.join(get_enc_path(config['ppxpath']), "encdata.ppx")).read() or "{}")

	if(args.command == "get"):
		check_cryptokey()
		X = D.get(args.name)
		if(X):
			print(decrypt(bytes(X, encoding='ascii'), cryptokey))
		else:
			print("No Such Password Identifier Could be Found")

	elif(args.command == "add" or args.command == "update"):
		check_cryptokey()
		if(args.object):
			D[args.name] = encrypt(args.object, cryptokey)[1].decode('ascii')
		elif(args.password):
			D[args.name] = encrypt(args.password, cryptokey)[1].decode('ascii')
		else:
			print("Please Include New Password using -o or -p Flags")

		save_enc()

	elif(args.command == 'del'):
		check_cryptokey()
		D.pop(args.name) #!Handle KeyError
		save_enc()

	elif(args.command == 'list'):
		check_cryptokey()
		PTable = PrettyTable(['Name', 'Password'])
		for K, V in D.items():
			PTable.add_row([K,  decrypt(bytes(V, encoding='ascii'), cryptokey)])
		print(PTable)

	elif(args.command == 'clear'):
		D.clear()
		save_enc()

	elif(args.command == 'config'):
		#PPXPathConfig
		if(args.ppxpath):
			#Updating  PPXPath
			if(args.ppxpath == "."):
				config['ppxpath'] = "base"
			else:
				config['ppxpath'] = os.path.join(args.ppxpath)

			#Create encfile if it doesnt exist
			if(not os.path.isfile(os.path.join(get_enc_path(config['ppxpath']), 'encdata.ppx'))):
				with open(os.path.join(get_enc_path(config['ppxpath']), 'encdata.ppx'), "w") as f:
					f.write(json.dumps({}))

			#Update Configuration
			save_config()


	#MINOR COMMANDS
	else:
		if(args.command == "cppxp"):
			print("Current Location of .ppx File:", get_enc_path(config['ppxpath']))
		# elif(args.command == "cryptoenv"):
		# 	config['crypto_env'] = True
		# 	#Add to ENV
		# 	os.environ['cryptoenv'] = "X"
		# 	print("X", os.environ['cryptoenv'])
		# 	save_config()
		else:
			print("Invalid Command")