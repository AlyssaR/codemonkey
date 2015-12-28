import ConfigParser, os

configs = {"install": {"linux": [], "windows": [], "services": []},
            "backup": {"linux": [], "windows": [], "services": []},
            "setup": {"linux": [], "windows": [], "services": []},
            "restore": {"linux": [], "windows": [], "services": []}}

def backup(stuff):
    print "backup"

def clean(stuff):
    print "clean"

def install(stuff):
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


def restore(stuff):
    print "restore"

def setup(stuff):
    print "setup"

def main():
    load_configs()
    print configs

if __name__ == '__main__': main()
