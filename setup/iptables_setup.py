import subprocess
import sys
import os

def dependencies():
	print
	print "-----------------------"
	print "Installing Dependencies"


def setup(tcp_ports, udp_ports):
	print
	print "-----------------------"
	print "Setting up Firewall..."

	#For this basic setup, we will create two user-defined chains that we will use to open up ports in the firewall.
	subprocess.Popen(["iptables", "-N", "TCP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-N", "UDP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#since this is a single machine and not nat, we drop forward
	subprocess.Popen(["iptables", "-P", "FORWARD", "DROP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#is there no intention of filtering outbound traffic?
	subprocess.Popen(["iptables", "-P", "OUTPUT", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#ceate a rule for keeping current sessions open
	#(as to not kick off those who are ssh'd in)
	subprocess.Popen(["iptables", "-A", "INPUT", "-m", "conntrack", "--ctstate", "RELATED,ESTABLISHED", "-j", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#now drop all incomming--will not *currently* allow new connections but will keep old ones open
	subprocess.Popen(["iptables", "-P", "INPUT", "DROP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#accept all loopback traffic
	subprocess.Popen(["iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#drop all packets with an 'invalid' state
	subprocess.Popen(["iptables", "-A", "INPUT", "-m", "conntrack", "--ctstate", "INVALID", "-j", "DROP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


	#Allow icmp echo requests. Only the first packet will count as NEW
	#the rest will be handled by the RELATED,ESTABLISHED rule
	subprocess.Popen(["iptables", "-A", "INPUT", "-p", "icmp", "--icmp-type", "8", "-m", "conntrack", "--ctstate", "NEW", "-j", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


	#Now we attach the TCP and UDP chains to the INPUT chain to handle all new incoming connections.
	#Once a connection is accepted by either TCP or UDP chain, it is handled by the RELATED/ESTABLISHED traffic rule.
	#The TCP and UDP chains will either accept new incoming connections, or politely reject them.
	#New TCP connections must be started with SYN packets.

	subprocess.Popen(["iptables", "-A", "INPUT", "-p", "udp", "-m", "conntrack", "--ctstate", "NEW", "-j", "UDP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-A", "INPUT", "-p", "tcp", "--syn", "-m", "conntrack", "--ctstate", "NEW", "-j", "TCP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)



	#Now for the real rules

	for number in tcp_ports:
		print "Port", number
		command = "iptables -A TCP -p tcp --dport " + number + " -j ACCEPT"
		print  command
		os.system(command)

	for number in udp_ports:
		print "Port", number
		command = "iptables -A UDP -p udp --dport " + number + " -j ACCEPT"
		print  command
		os.system(command)


	#now supposedly protection against spoofing attacks? + logging
	subprocess.Popen(["iptables", "-t", "raw", "-I", "PREROUTING", "-m", "rpfilter", "--invert", "-j", "DROP"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

	#For other protocols, we add a final rule to the INPUT chain to reject all remaining incoming
	#traffic with icmp protocol unreachable messages. This imitates Linux's default behavior.

	##NOTE: This may be a bad idea.. if something is of a different protocol than icmp/tcp/udp we may be screwed with this rule...?

	subprocess.Popen(["iptables", "-A", "INPUT", "-j", "REJECT", "--reject-with", "icmp-proto-unreachable"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)



	show()



def createBackup(fileName):
	print
	print "-----------------------"
	print "Creating Backup Located At:", fileName
	command = "iptables-save > " + fileName
	os.system(command)



def restoreFromBackup(fileName):
	print
	print "-----------------------"
	print "Restoring Backup From File:", fileName
	print fileName

	#insecure need to find a way with subprocesses
	#also would like to see if the file is there... error handling!
	command = "iptables-restore < " + fileName
	os.system(command)
	show()


def clear():
	print
	print "Clearing iptables rules and loading defaults"
	subprocess.Popen(["iptables", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-X"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "nat", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "nat", "-X"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "mangle", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "mangle", "-X"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "raw", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "raw", "-X"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "security", "-F"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-t", "security", "-X"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-P", "INPUT", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-P", "FORWARD", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	subprocess.Popen(["iptables", "-P", "OUTPUT", "ACCEPT"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	show()


def show():
	print "Running 'iptables -nvL --line-numbers'...\n"
	p = subprocess.Popen(["iptables", "-nvL", "--line-numbers"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	output = p.stdout.read()
	print output


def menu():
	while True:
		print "=========================="
		print "What would you like to do?"
		print "1). Install FW Dependencies"
		print "2). Setup FW"
		print "3). Create FW Backup"
		print "4). Restore FW From Backup"
		print "5). Clear FW"
		print "6). Show Current FW"
		print "0). Exit"

		choice = input("Choice: ")

		if choice == 1:
			dependencies()

		elif choice == 2:
			tcp_ports = []
			udp_ports = []

			while True:
				portNumber = raw_input("Open TCP Ports? (0 to move on): ")
				if portNumber == "0":
					break
				else:
					tcp_ports.append(portNumber)

			while True:
				portNumber = raw_input("Open UDP Ports? (0 to move on): ")
				if portNumber == "0":
					break
				else:
					udp_ports.append(portNumber)

			setup(tcp_ports, udp_ports)

		elif choice == 3:
			fileName = raw_input("What would you like the filename to be?: ")
			print fileName
			restoreFromBackup(fileName)
			createBackup(fileName)

		elif choice == 4:
			print "Printing Files in Current Dir"
			p = subprocess.Popen(["ls", "-lah"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
			output = p.stdout.read()
			print output
			fileName = raw_input("What is the file path?: ")
			print fileName
			restoreFromBackup(fileName)

		elif choice == 5:
			clear()

		elif choice == 6:
			show()

		elif choice == 0:
			sys.exit("User Exited")



def main():

	menu()

	return 0


if __name__ == '__main__': main()
