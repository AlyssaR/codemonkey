import getpass, os, platform, subprocess, sys

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    print "[+] Installing Elk..."
    os_version = float(platform.linux_distribution()[1])
    os_name = get_os_name(os_version)
    ip = [x[1] for x in args if x[0] == "localip"][0]

    """System Check"""
    if platform.linux_distribution()[0] != "Ubuntu":
        return "Ubuntu expected."
    if not os_name:
        return "Not acceptable version of Ubuntu."
    if platform.architecture()[0] != "64bit":
        return "64bit OS required."
    if not check_kernel(os_name): #needs testing!
        return "Kernel less than required version. Please reboot to finish upgrade."
    if ip == "test": #Check if only test run
        return
    print "[+] System check passed"

    """Install Docker Dependencies"""
    subprocess.Popen(["apt-key", "adv", "--keyserver", "hkp://p80.pool.sks-keyservers.net:80", "--recv-keys", \
                    "58118E89F3A912897C070ADBF76221572C52609D"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Add GPG key
    with open("/etc/apt/sources.list.d/docker.list", "w+") as docker_list: #Update apt list
        docker_list.write("deb https://apt.dockerproject.org/repo ubuntu-" + os_name + " main")
    subprocess.Popen(["apt-get", "update"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Refresh apt lists
    subprocess.Popen(["apt-get", "purge", "lxc-docker"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    subprocess.Popen(["apt-cache", "policy", "docker-engine"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    print "[+] Got docker-engine dependencies"

    if os_name != "precise":
        #subprocess.Popen(["apt-get", "update"], stdin=subprocess.PIPE).wait() #Refresh apt lists
        image = "linux-image-extra-" + platform.release()
        subprocess.Popen(["apt-get", "install", image, "-y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Update kernel
    print "[+] Updated kernel"

    """Install Docker-Engine and Docker-Compose"""
    #subprocess.Popen(["apt-get", "update"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Refresh apt lists
    subprocess.Popen(["apt-get", "install", "docker-engine", "-y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait() #Install docker-engine
    os.system("curl -L https://github.com/docker/compose/releases/download/1.5.2/docker-compose-" \
                    + platform.system() + "-" + platform.machine() + " > /usr/local/bin/docker-compose")
    os.system("chmod +x /usr/local/bin/docker-compose") #Install docker-compose
    print "[+] Installed docker-engine and docker-compose"

    """Add root to Docker group"""
    subprocess.Popen(["usermod", "-aG", "docker", getpass.getuser()], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()

    """Config Docker with IP Address"""
    with open("./resources/elk/docker-compose.yml", "a") as compose_file:
        compose_file.write("\t\tELASTICSEARCH_URL: http://" + ip + ":9200")
    with open("./resources/elk/logstash/logstash.conf", "a") as logstash_file:
        logstash_file.write("output {\n\telasticsearch {\n\t\thosts => [\"" + ip + "\"]\n\t}\n}")
    print "[+] Added IP address to docker configs"

    print "[!] You must log out and log back in before you can start docker-engine or run the elk setup module."
    return

def check_kernel(os_name):
    proc = subprocess.Popen(["uname", "-r"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    version = float(proc.communicate()[0][:3])
    if version < 3.1:
        print "[!] Kernel needs update"
        proc = subprocess.Popen(["apt-get", "update", "&&", "dist-upgrade", "-y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print "[*] Please restart system and re-run module with updated kernel."
        return False
    elif os_name == "precise" and version < 3.13:
        print "[!] Precise requires kernel >= 3.13"
        proc = subprocess.Popen(["apt-get", "update", "&&", "apt-get", " install", "linux-image-generic-lts-trusty", "-y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print "[*] Please restart system and re-run module with updated kernel."
        return False
    else:
        return True

def get_os_name(os_version):
    if isclose(os_version, 12.04):
        return "precise"
    elif isclose(os_version, 14.04):
        return "trusty"
    elif isclose(os_version, 15.04):
        return "vivid"
    elif isclose(os_version, 15.10):
        return "wily"
    else:
        return

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def main():
    print "Testing system"
    result = run([("localip", "test")])
    if not result:
        print "System OK."
    else:
        print "[!] Error", result

if __name__ == '__main__': main()
