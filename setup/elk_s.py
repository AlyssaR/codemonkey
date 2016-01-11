import getpass, os, platform, pwd, subprocess

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    os_version = float(platform.linux_distribution()[1])

    """Create Docker User"""
    user_name = [x[1] for x in args if x[0] == "username"][0]
    if not user_name:
        return "No username provided in config."
    os.system("useradd -G sudo,docker " + user_name)
    subprocess.Popen(["passwd", user_name]).wait()
    #password = raw_input("Enter new password: ")
    #print password
    #os.system("echo -e " + password + "\\n" + password + " | passwd " + user_name)

    return

    """Start Docker-Engine as New User"""
    try:
        pw_record = pwd.getpwnam(user_name)
    except:
        return "Could not get user", user_name
    return
    env = os.environ.copy()
    env['HOME']  = pw_record.pw_dir
    env['LOGNAME']  = pw_record.pw_name
    env['PWD']  = os.getcwd()
    env['USER']  = pw_record.pw_name
    subprocess.Popen(["service", "docker", "start"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, \
                    preexec_fn=demote(user_uid, user_gid), cwd=cwd, env=env).wait()

    """Start Docker-Engine and Compose DockerFile"""
    os.system("cd resources/elk")
    subprocess.Popen(["docker-compose", "up", "-d"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()
    os.system("cd ../..")
    print "[+] Composed appliances"

    """Set to Start on Boot"""
    if os_version > 15:
        subprocess.Popen(["systemctl", "enable", "docker"], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()

    """Change Default Passwords"""

    """Change Default Ports?"""

    return "Module not completed yet."

def demote(user_uid, user_gid):
    os.setgid(user_gid)
    os.setuid(user_uid)
    subprocess.Popen(["usermod", "-aG", "docker", getpass.getuser()], stdin=subprocess.PIPE, stdout=subprocess.PIPE).wait()

def main():
    print "Testing system"
    print run([("username", "elk")])

if __name__ == '__main__': main()
