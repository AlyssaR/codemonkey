def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    check = input("Have you logged out and logged back in since running the elk install module? (y/n) ")
    if check[0] == 'n' or check[0] == 'N':
        return "Please log out/in and run again."

    """Start Docker-Engine and Compose DockerFile"""
    subprocess.Popen(["service", "docker", "start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    os.system("cd resources/elk")
    subprocess.Popen(["docker-compose", "up", "-d"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Run
    os.system("cd ../..")
    print "[+] Composed appliances"

    return "Module not completed yet."
