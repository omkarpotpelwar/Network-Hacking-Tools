import socket
import os
import sys

def dns():

	while True:
		dom = input('Enter domain: ')
		print(socket.gethostbyname(dom))

		if dom == 'q':
			print('done!')
			break

def reverse_dns():
	try:
		ip = input('Enter IP: ')
		res = socket.gethostbyaddr(ip)
		print("Address: ")
		print("\nThe host name is : ")
		print(" " + res[0])
		for i in res[2]:
			print(" " + i)
	except socket.herror:
		print("Error resolving IP address: " + e)

print('1] Domain to IP \n2] IP to domain')
x = input()
if x == '1':
	dns()
else:
	reverse_dns()