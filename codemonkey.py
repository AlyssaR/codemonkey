import ConfigParser, os

configs = {"install": [], "backup": [], "setup": [], "restore": []}

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
    configs["backup"] = config.get("dirs", "backup").split(",")
    configs["install"] = config.get("dirs", "install").split(",")
    configs["restore"] = config.get("dirs", "restore").split(",")
    configs["setup"] = config.get("dirs", "setup").split(",")

def restore(stuff):
    print "restore"

def setup(stuff):
    print "setup"

def main():
    load_configs()

if __name__ == '__main__': main()
