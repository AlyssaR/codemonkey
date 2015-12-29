import os, platform, subprocess, sys

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    print "[+] Installing Elk..."
    os_version = float(platform.linux_distribution()[1])
    ip = [x[1] for x in args if x[0] == "localip"][0]


    """System Check"""
    if platform.linux_distribution()[0] != "Ubuntu":
        return "Ubuntu expected."
    if platform.architecture()[0] != "64bit":
        return "64bit OS required."
    if not check_kernel(): #needs testing!
        return "Kernel less than required version (>= 3.1)."
    if ip == "test": #Check if only test run
        return

    """Install Docker-Engine and Docker-Compose"""
    if os_version < 0:
        print "sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D"


    """Create Docker User"""

    """Config Docker with IP Address"""
    with open("./resources/elk/docker_compose.yml", "a") as compose_file:
        compose_file.write("\t\tELASTICSEARCH_URL: http://" + ip + ":9200")
    with open("./resources/elk/logstash/logstash.conf", "a") as logstash_file:
        logstash_file.write("output {\n\telasticsearch {\n\t\thosts => [\"" + ip + "\"]\n\t}\n}")

    """Compose DockerFile"""

    """Security Configurations for ELK Stack"""

    return

def check_kernel():
    proc = subprocess.Popen(["uname", "-r"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    version = float(proc.communicate()[0][:3])
    if version < 3.1:
        print "[!] Kernel needs update"
        proc = subprocess.Popen(["apt-get", "update", "&&", "dist-upgrade", "-y"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print "[*] Please restart system and re-run module with updated kernel."
        return False
    else:
        return True

def main():
    print "Testing system"
    result = run([("localip", "test")])
    if not result:
        print "System OK."
    else:
        print "[!] Error", result


if __name__ == '__main__': main()
