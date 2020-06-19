#!/bin/python3
import socket
import sys
from datetime import datetime as dt


subdomains_count = 0
if len(sys.argv) == 2:
	subdomains = []
	
	
	file = open(sys.argv[1], 'r');
	
	for subdomain in file:
		subdomain = subdomain.strip('\n')
		
		if subdomain != '':
			subdomains.append(subdomain)
			subdomains_count += 1
	file.close()
else:
	print("Usage: ./{} <subdomains_file>".format(sys.argv[0]))
	sys.exit()


def report():
	print('\n')
	print('-' * 50)
	print("Scanning started {}".format(dt.now()))
	print('-' * 50)
	print('\n')


report()
alive_subdomains = []
for index in range(0, subdomains_count):
	try:
		target = socket.gethostbyname(subdomains[index]) #translate hostname to IPv4
		default_ports = [80, 443]
		
		for port in default_ports:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			
			socket.setdefaulttimeout(1)
			status = s.connect_ex((target, port))
			
			if status == 0:
				alive_subdomains.append((subdomains[index], port))
			s.close()
	except KeyboardInterrupt:
		print("\nExiting the program.")
		sys.exit()
	except socket.gaierror:
		print("\nHostname could not be resolved: " + subdomains[index])
		continue
	except socket.error:
		print("\nCould not connect to server")
		continue
		
print("Alive subdomains")

for subdomain in alive_subdomains:
	print(subdomain)
	
	
file = open("new_subdomain.txt", 'w')

for subdomain in alive_subdomains:
	file.write(subdomain[0] + '\n')
file.close()

report()
