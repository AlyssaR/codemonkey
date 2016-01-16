import getpass, os, platform, socket, subprocess, datetime

def run():
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """

    print "\n******************************************"
    print "SUMMARY"
    print "******************************************"
    print "{:<15} {:<20}".format('Hostname', platform.node())
    print "{:<15} {:<20}".format('IP Address', ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]))
    print "{:<15} {:<20}".format('OS', platform.platform(terse=True))
    print "{:<15} {:<20}".format('Platform', platform.architecture()[0])


    print "\n******************************************"
    print "USERS"
    print "******************************************"
    print "{:<20} {:<10} {:<10} {:<15} {:<10}".format('Username','User ID', 'Group ID', 'Shell', 'Groups')
    print "--------------------------------------------------------------------------"
    
    for user in getUsers():
        print "{:<20} {:<10} {:<10} {:<15}".format(user[0],user[2],user[3],user[6]), ", ".join(user[7])


    print "\n******************************************"
    print "SERVICES"
    print "******************************************"
    for service in getServices():
        print service

    print "\n******************************************"
    print "OPEN/ESTABLISHED CONNECTIONS"
    print "******************************************"
    for line in getConnections():
        print line


    print "\n******************************************"
    print "BACKING UP BASH HISTORY FOR KNOWN USERS"
    print "******************************************"
    getBashHistory(getUsers())

    return


def getConnections():
    #Run command
    netstat = subprocess.Popen(["netstat", "-ntlp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    results = netstat.communicate()[0].split("\n")

    return results



def getServices():

    #checks init.d directory for common words:
    #web, apache, http, sql, lite, ssh, bind, ftp, 
    #dns, vpn, nfs, nmbd, samba, smbd, snmp, smtp
    servicesList = []

    initDir = subprocess.Popen(["ls", "/etc/init.d"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate()[0].split('\n')

    for service in initDir:
        if (("web" in service) or ("apache" in service) or +
        ("http" in service) or ("sql" in service) or ("lite" in service) +
        ("ssh" in service) or ("bind" in service) or ("ftp" in service) +
        ("dns" in service) or ("vpn" in service) or ("nfs" in service) +
        ("nmbd" in service) or ("samba" in service) or ("smbd" in service) +
        ("snmp" in service) or ("smtp" in service)):
            servicesList.append(service)

    return servicesList


def getUsers():
    #Local users
    #In linux I am making this any user in passwd file that can access a shell
    lines = []
    userList = []

    passwdFile = open('/etc/passwd')
    while True:
        line = passwdFile.readline()
        line = line.strip('\n')
        if not line:
            break
        elif not "/bin/false" in line:
            if not "nologin" in line:
                userList.append(line.split(":"))

    #Now compare the gorupID and userID to the gorups file    
    for user in userList:
        #Note that userID is at user[2]
        #Note that groupID is at user[3]
        groups = []
        groupFile = open('/etc/group')

        while True:
            line = groupFile.readline()
            if not line:
                break
            elif (':' + user[2] + ':') and (':' + user[3] + ':') in line:
                #print "checking if :" + user[2] + ": is in", line
                #print "checking if :" + user[3] + ": is in", line
                groups.append(line.split(":")[0])
            if (':' + user[0] + ':') in line:
                groups.append(line.split(":")[0])

        user.append(groups)

    return userList


def getBashHistory(userList):

	#check to see if dir exists for bash history
	if not os.path.isdir("archive/bash_history"):
		os.makedirs("archive/bash_history")


	usersToBackupHistory = []

	print "{:<20} {:<30} {:<20}".format('Username','Home Directory', '.bash_history exists?')
	print "--------------------------------------------------------------------------"
    
	for user in userList:
		if os.path.exists(user[5] + "/.bash_history"):
			print "{:<20} {:<35} {:<20}".format(user[0],user[5],"y")
			usersToBackupHistory.append(user)
		else:
			print "{:<20} {:<35} {:<20}".format(user[0],user[5],"n")

	print 
	print "Backing up bash_history for users with an existing file"
	print "--------------------------------------------------------------------------"
	for user in usersToBackupHistory:
		subprocess.Popen(["cp", (user[5] + "/.bash_history"), ("archive/bash_history/" + user[0] + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M_") + str(datetime.datetime.now().second) + ".txt")], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
		print user[0], "done"

	return True


def main():
    print ">>> Testing System <<<"
    
    result = run()
    
    if result:
        print "[!] Error", result


if __name__ == '__main__': main()


