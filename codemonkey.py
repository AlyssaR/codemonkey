import ConfigParser, imp, os, sys

isWindows = True if (os.name == "nt") else False
configs = {"install": {"linux": [], "windows": [], "services": []},
            "backup": {"linux": [], "windows": [], "services": []},
            "setup": {"linux": [], "windows": [], "services": []},
            "restore": {"linux": [], "windows": [], "services": []}}
if isWindows:
    sys.path.append(os.getcwd() + "\\backup")
    sys.path.append(os.getcwd() + "\\install")
    sys.path.append(os.getcwd() + "\\restore")
    sys.path.append(os.getcwd() + "\\setup")
else:
    sys.path.append("./backup")
    sys.path.append("./install")
    sys.path.append("./restore")
    sys.path.append("./setup")

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

def restore():
    print "restore"

def setup():
    moduleNames = [x[0:-3] for x in os.listdir("setup") if x[-1] != 'c']
    for mod in moduleNames:
        imp.load_source(mod, ".\\setup") 

    testmodule.test()

def main():
    load_configs()
    setup()

if __name__ == '__main__': main()
