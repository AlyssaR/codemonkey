import os, platform, socket, subprocess

def run():
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    isServer = True if "server" in platform.release().lower() else False


    print "\n******************************************"
    print "SUMMARY"
    print "******************************************"
    print "{:<15} {:<20}".format('Hostname', platform.node())
    print "{:<15} {:<20}".format('IP Address', socket.gethostbyname(socket.gethostname()))
    print "{:<15} {:<20}".format('OS', platform.platform(terse=True))
    print "{:<15} {:<20}".format('Platform', platform.architecture()[0])


    print "\n******************************************"
    print "USERS"
    print "******************************************"
    print "{:<20} {:<6}".format('Username','Admin?')
    print "---------------------------"
    for u, a in sorted(getUsers().items()):
        print "{:<20} {:<6}".format(u, 'Yes' if a else 'No')


    if isServer:
        print "\n******************************************"
        print "SERVICES"
        print "******************************************"
        for s in getServices():
            print s


    print "\n******************************************"
    print "OPEN/ESTABLISHED CONNECTIONS"
    print "******************************************"
    ports = getPorts()
    #Only does common ports
    # tcp = sorted( list(set( [int(x["src"]) for x in ports["tcp"] if int(x["src"]) < 1024] )) )
    # udp = sorted( list(set( [int(x["src"]) for x in ports["udp"] if int(x["src"]) < 1024] )) )

    #Does all ports
    tcp = sorted( list(set( [int(x["src"]) for x in ports["tcp"]] )) )
    udp = sorted( list(set( [int(x["src"]) for x in ports["udp"]] )) )

    print "------\nTCP\n------"
    if len(tcp) > 0:
        for t in tcp:
            print t
    else:
        print "No open ports."
    print "------\nUDP\n------"
    if len(udp) > 0:
        for u in udp:
            print u
    else:
        print "No open ports."


    """ Do we want this?
    print "\n******************************************"
    print "INSTALLED PATCHES"
    print "******************************************"
    for p in getPatches():
        print p
    """


    return

def getPatches():
    return ["Not complete"]

def getPorts():
    #Run command
    netstat = subprocess.Popen(["netstat", "-an"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    results = netstat.communicate()[0].split("\r\n")[4:]

    #Format results
    tcp = []
    udp = []
    for r in results:
        x = filter(None, r.split(" "))
        if len(x) < 4:
            continue

        if x[0].lower() == "tcp":
            if x[3].lower() != "established" and x[3].lower() != "listening":
                continue
            tcp.append({"src":x[1].split(":")[-1], "dst":x[2], "state":x[3]})
        else:
            udp.append({"src":x[1].split(":")[-1], "dst":x[2], "state":x[3]})

    return {"tcp": tcp, "udp": udp}

def getServices():
    opersys = platform.platform(terse=True)
    results = []
    if "2012" in opersys:
        #Get-WindowsFeature
        print "2012"
    else:
        print "I hate life."
        #os.system("servermanagercmd -query")
        #proc = subprocess.Popen(["powershell", "-command", "\"servermanagercmd -query\""], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #print proc.communicate()[0]

    return results

def getUsers():
    #Local users
    user_proc = subprocess.Popen(["net", "user"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    users = user_proc.communicate()[0].split("\r\n")
    start = users.index([x for x in users if "---" in x][0]) + 1
    end = users.index("The command completed successfully.")
    users = {x:False for x in filter(None, " ".join(users[start:end]).split(" "))}

    #Find Local Admins
    admin_proc = subprocess.Popen(["net", "localgroup", "administrators"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    admins = admin_proc.communicate()[0].split("\r\n")
    start = admins.index([x for x in admins if "---" in x][0]) + 1
    end = admins.index("The command completed successfully.")
    for x in filter(None, admins[start:end]):
        users[x] = True

    return users

def main():
    print ">>> Testing System <<<"
    print "**WARNING: OS version will return incorrectly for systems above " + \
            "Windows 8 because Microsoft is dumb.\n"
    result = run()
    if result:
        print "[!] Error", result

if __name__ == '__main__': main()
