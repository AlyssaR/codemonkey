import getpass

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    check = input("Have you logged out and logged back in since running the elk install module? (y/n) ")
    if check[0] == 'n' or check[0] == 'N':
        return "Please log out/in and run again."

    """Create User for Docker"""

    """Start Docker-Engine and Compose DockerFile"""
    subprocess.Popen(["service", "docker", "start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    os.system("cd resources/elk")
    subprocess.Popen(["docker-compose", "up", "-d"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    os.system("cd ../..")
    print "[+] Composed appliances"

    """Set to Start on Boot"""

    """Change Default Passwords"""

    """Change Default Ports?"""

    return "Module not completed yet."

def main():
    print "Testing system"
    print getpass.getuser()

if __name__ == '__main__': main()
