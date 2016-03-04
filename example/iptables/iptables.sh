#!/bin/bash

#ls -lah

#date +%m_%d_5y-%H.%M.%S

function setup {
	echo "Running Setup Script"
	echo "---------------------------"

	echo
	echo "Please enter the TCP ports you wish to be open (one at a time, -1 to break):"

	declare -a tcpPorts

	port="0"
	while [ $port -ne "-1" ]
	do
		read -p "Port:  " port

		if [ $port -ne "-1" ]; then
			#Add port to tcp port array
			tcpPorts=("${tcpPorts[@]}" "$port")
		fi
	done


	echo
	echo "Please enter the UDP ports you wish to be open (one at a time, -1 to break):"

	declare -a udpPorts

	port="0"
	while [ $port -ne "-1" ]
	do
		read -p "Port:  " port

		if [ $port -ne "-1" ]; then
			#Add port to tcp port array
			udpPorts=("${udpPorts[@]}" "$port")
		fi
	done

	echo
	echo "TCP:"
	echo ${tcpPorts[@]}
	echo
	echo "UDP:"
	echo ${udpPorts[@]}

	#First create a current backup
	createBackup

	#Next Clear the Firewall
	clear

	#Finally implement actual rules
	#For this basic setup, we will create two user-defined chains that we will use to open up ports in the firewall.
	iptables -N TCP
	iptables -N UDP

	#since this is a single machine and not nat, we drop forward
	iptables -P FORWARD DROP

	#is there no intention of filtering outbound traffic?
	iptables -P OUTPUT ACCEPT

	#ceate a rule for keeping current sessions open
	#(as to not kick off those who are ssh'd in)
	iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT

	#now drop all incomming--will not *currently* allow new connections but will keep old ones open
	iptables -P INPUT DROP

	#accept all loopback traffic
	iptables -A INPUT -i lo -j ACCEPT

	#drop all packets with an 'invalid' state
	iptables -A INPUT -m conntrack --ctstate INVALID -j DROP


	#Allow icmp echo requests. Only the first packet will count as NEW
	#the rest will be handled by the RELATED,ESTABLISHED rule
	iptables -A INPUT -p icmp --icmp-type 8 -m conntrack --ctstate NEW -j ACCEPT


	#Now we attach the TCP and UDP chains to the INPUT chain to handle all new incoming connections.
	#Once a connection is accepted by either TCP or UDP chain, it is handled by the RELATED/ESTABLISHED traffic rule.
	#The TCP and UDP chains will either accept new incoming connections, or politely reject them.
	#New TCP connections must be started with SYN packets.
	iptables -A INPUT -p udp -m conntrack --ctstate NEW -j UDP
	iptables -A INPUT -p tcp --syn -m conntrack --ctstate NEW -j TCP



	echo "Now opening User defined ports"
	echo "---------------------------"

	for i in "${tcpPorts[@]}"
	do
	   :
	   echo "Opening TCP port $i"
	   iptables -A TCP -p tcp --dport $i -j ACCEPT
	done


	for i in "${udpPorts[@]}"
	do
	   :
	   echo "Opening UDP port $i"
	   iptables -A UDP -p udp --dport $i -j ACCEPT
	done

	#now supposedly protection against spoofing attacks? + logging
	iptables -t raw -I PREROUTING -m rpfilter --invert -j DROP

	#For other protocols, we add a final rule to the INPUT chain to reject all remaining incoming
	#traffic with icmp protocol unreachable messages. This imitates Linux's default behavior.

	##NOTE: This may be a bad idea.. if something is of a different protocol than icmp/tcp/udp we may be screwed with this rule...?
	iptables -A INPUT -j REJECT --reject-with icmp-proto-unreachable

	#Reshow all rules
	show

	echo "All Rules Successfully Implemented"
}


function createBackup {
	echo "Creating Backup of Current IP Tables"
	echo "---------------------------"
	if [ ! -d "archive/Firewall" ]; then
  		mkdir archive
  		mkdir archive/Firewall
	fi
		fileName="archive/Firewall/iptables_backup_"$(date +%m_%d_%y-%H.%M.%S)
		echo "Creating backup at $fileName"
		iptables-save > $fileName
}

function restoreFromBackup {
	echo "Restoring Backup of Current IP Tables"
	echo "---------------------------"
	if [ ! -d "archive/Firewall" ]; then
  		mkdir archive
  		mkdir archive/Firewall
	fi
		echo "Which file would you like to restore? (Showing files from archive/Firewall/)"
		ls archive/Firewall/
		echo ""
		echo "Which filename would you like to restore?:"
		read fileName
		echo "Restoring from $fileName"
		iptables-restore < archive/Firewall/$fileName
}


function clear {
	echo "Clearing Current IP Tables and Loading Defaults"
	echo "---------------------------"
	iptables -F
	iptables -X
	iptables -t nat -F
	iptables -t nat -X
	iptables -t mangle -F
	iptables -t mangle -X
	iptables -t raw -F
	iptables -t raw -X
	iptables -t security -F
	iptables -t security -X
	iptables -P INPUT ACCEPT
	iptables -P FORWARD ACCEPT
	iptables -P OUTPUT ACCEPT

	# Run the show function
	show
}


function show {
	echo "Showing Current IP Tables"
	echo "---------------------------"
	echo "Running: 'iptables -nvl --line-numbers'... "
	iptables -nvL --line-numbers

}


function menu {
	echo 'This is the IP Tables Script (In Bash Form!)'

	options=("setup" "show" "clear" "backup" "restore" "Quit")
	echo 'Please enter your choice: '
	select opt in "${options[@]}"

	do
	    case $opt in
	        "setup")
	            setup
	            ;;
	        "show")
	            show
	            ;;
	        "clear")
	            clear
	            ;;
	        "backup")
	            createBackup
	            ;;
	        "restore")
	            restoreFromBackup
	            ;;
	        "Quit")
	            break
	            ;;
	        *) echo invalid option;;
	    esac

	done

}



menu

