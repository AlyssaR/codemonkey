"""     CodeMonkey
    authors:        Alyssa Rahman
    last updated:   2016-01-04

    description:
        This suite is intended to help automate system setup, hardening, and administration.

    usage: ./codemonkey.py [OPTIONAL: go] [OPTIONAL: file.config]

        Passing "go" as the first argument will run an initial system setup.
            If not specified, a menu will be brought up to run specific functions.

        Passing a path to a config file will load those configs.
            If not specified, default config will be loaded.
            If unable to load or default not found, will exit.
"""

import ConfigParser, imp, os, sys

isWindows = True if (os.name == "nt") else False
configfile = ConfigParser.ConfigParser()
configs = {"install": {"folders": [], "services": []},
            "backup": {"folders": [], "services": []},
            "clean": {"folders": [], "services": []},
            "setup": {"folders": [], "services": []},
            "resources": {"folders": [], "services": []},
            "restore": {"folders": [], "services": []}}

def initial_setup():
    print "Not done yet..."

def load_configs():
    if len(sys.argv) == 1 or sys.argv[1].lower() == "go":
        print "[!] Warning: No config file specified. Using default."
        if os.path.isfile("default.conf"):
            configfile.read("default.conf")
        else:
            return "[!] Error: default.conf not found. Exiting.."
    else:
        if os.path.isfile(sys.argv[-1]):
            configfile.read(sys.argv[-1])
        else:
            return "[!] Could not load config file", sys.argv[-1]

    for section in configs:
        if section == "backup":
            try:
                configs[section]["folders"] = configfile.get(section, "folders").split(",")
            except:
                print "[?] No folders variable in", section

        try:
            configs[section]["services"] = configfile.get(section, "services").split(",")
        except:
            print "[?] No Services in", section

def load_modules(directory):
    module_names = [x for x in os.listdir(directory) if x[-1] != 'c' and x[-2:] == "py"]
    cur_dir = (".\\" + directory +"\\") if isWindows else ("./" + directory + "/")
    for mod in module_names:
        imp.load_source(mod[:-3], cur_dir + mod)

    return [x[:-3] for x in module_names]

def run_modules(mode, module_names):
    for mod in module_names:
        prefix = mod[:3]
        isService = False if prefix == "lin" or prefix == "win" else True

        """Skip incompatible modules"""
        if (isWindows and prefix == "lin") or (not isWindows and prefix == "win"):
            continue

        if not isService:
            print "[+] Running", mod

        """If module is a service, retrieve additional args"""
        if mode == "backup" and mod.split('_')[0] == "folders":
            result = sys.modules[mod].run(configs[mode]["folders"])
        elif isService: #if it is a service it has to have a section in the config file
            if mod.split('_')[0] not in configs[mode]["services"]:
                continue
            print "[+] Running", mod
            try:
                mod_configs = configfile.items(mod.split('_')[0])
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
            result = sys.modules[mod].run(mod_configs)
        else: #if it's not a service it has no arguments
            result = sys.modules[mod].run()

        """Display results"""
        if(result):
            print "[!] Error", result
        else:
            print "[+] Success!"

def test(args):
    print ">>> Test Example Modules <<<"
    module_names = load_modules("example")

    for mod in module_names:
        print "[+] Running", mod
        result = sys.modules[mod].run(args)
        if(result):
            print "[!] Error", result
        else:
            print "[*] Success!"

def main():

    if not os.path.isdir("archive"): #create archive directory if it doesn't exist
        os.makedirs("archive")

    result = load_configs()
    if result:
        print result
        return

    if len(sys.argv) > 1 and sys.argv[1].lower() == "go":
        print ">>> Performing Initial System Setup <<<"
        initial_setup()

    while True:
        print "\n----- MENU -----"
        print "1) Install"
        print "2) Setup"
        print "3) Backup"
        print "4) Restore"
        print "5) Clean"
        print "6) Resources/Profile"
        print "7) USAGE OK RUSSELL"
        print "0) Exit"

        choice = input("Choice: ")
        if choice == 1:
            print ">>> Install <<<"
            run_modules("install", load_modules("install"))
        elif choice == 2:
            print ">>> Setup <<<"
            run_modules("setup", load_modules("setup"))
        elif choice == 3:
            print ">>> Backup <<<"
            run_modules("backup", load_modules("backup"))
        elif choice == 4:
            print ">>> Restore <<<"
            run_modules("restore", load_modules("restore"))
        elif choice == 5:
            print ">>> Clean <<<"
            run_modules("clean", load_modules("clean"))
        elif choice == 6:
            print ">>> Info <<<"
            run_modules("resources", load_modules("resources"))
        elif choice == 7:
            print "\tCodeMonkey\nauthors:        Alyssa Rahman\nlast updated:   2016-01-04"
            print "description:\n\tThis suite is intended to help automate system setup, hardening, and administration."
            print "usage: ./codemonkey.py [OPTIONAL: go] [OPTIONAL: file.config]"
            print "\tPassing \"go\" as the first argument will run an initial system setup."
            print "\t\tIf not specified, a menu will be brought up to run specific functions."
            print "\t\tPassing a path to a config file will load those configs."
            print "\t\t\tIf not specified, default config will be loaded."
            print "\t\t\tIf unable to load or default not found, will exit."
        elif choice == 0:
            return
        else:
            print "Invalid choice. Try again."

if __name__ == '__main__': main()
