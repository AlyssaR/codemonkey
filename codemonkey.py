import ConfigParser, imp, os, sys

isWindows = True if (os.name == "nt") else False
configs = {"install": {"linux": [], "windows": [], "services": []},
            "backup": {"linux": [], "windows": [], "services": []},
            "setup": {"linux": [], "windows": [], "services": []},
            "restore": {"linux": [], "windows": [], "services": []}}

def backup():
    print "backup"

def clean():
    print "clean"

def install():
    print "install"
    #for script in listdir(./install):
        #temp = open(script)
        #result = temp.run()
        #result is some error code/status

def load_configs():
    config = ConfigParser.ConfigParser()
    config.read("config")

    for section in configs:
        try:
            configs[section]["linux"] = config.get(section, "linux").split(",")
        except:
            print "[?] No Linux variable in", section

        try:
            configs[section]["windows"] = config.get(section, "windows").split(",")
        except:
            print "[?] No Windows variable in", section

        try:
            configs[section]["services"] = config.get(section, "services").split(",")
        except:
            print "[?] No Services in", section

def load_modules(dir):
    module_names = [x for x in os.listdir("setup") if x[-1] != 'c']
    cur_dir = ".\\setup\\" if isWindows else "./setup/"
    for mod in module_names:
        imp.load_source(mod[0:-3], cur_dir + mod)

    return [x[0:-3] for x in module_names]

def restore():
    print "restore"

def setup():
    print ">>> Set Up <<<"
    module_names = load_modules("setup")

    for mod in module_names:
        print "[+] Running", mod
        sys.modules[mod].setup(["22", "80"], ["53"])

def main():
    load_configs()
    setup()

if __name__ == '__main__': main()
