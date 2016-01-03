import platform, socket

def run():
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    hostname = platform.node() #also domain
    os_ver = platform.release() #Version of OS
    platform = platform.architecture()[0] #32 or 64 bit
    ip_addr = socket.gethostbyname(socket.gethostname()) #IP address
    
    Patches Installed
    Users (admin/user)
    Services/Roles
    Ports Open

def main():
    print "Testing system"
    result = run()
    if not result:
        print "Collected System Profile"
    else:
        print "[!] Error", result

if __name__ == '__main__': main()
