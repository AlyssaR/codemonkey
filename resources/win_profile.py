import platform, socket, subprocess

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
    for u, a in getUsers().items():
        print "{:<20} {:<6}".format(u, 'Yes' if a else 'No')

    if isServer:
        print "\n******************************************"
        print "SERVICES"
        print "******************************************"
        for s in getServices():
            print s

    print "\n******************************************"
    print "OPEN/LISTENING PORTS"
    print "******************************************"
    for p in getPorts():
        print p

    print "\n******************************************"
    print "INSTALLED PATCHES"
    print "******************************************"
    for p in getPatches():
        print p

    return "Module not complete."

def getPatches():
    return ["Not complete"]

def getPorts():
    return ["Not complete"]

def getServices():
    return ["Not complete"]

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
    if not result:
        print "Collected System Profile"
    else:
        print "[!] Error", result

if __name__ == '__main__': main()
