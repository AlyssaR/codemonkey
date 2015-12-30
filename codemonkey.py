import ConfigParser, imp, os, sys

isWindows = True if (os.name == "nt") else False
configfile = ConfigParser.ConfigParser()
configs = {"install": {"folders": [], "services": []},
            "backup": {"folders": [], "services": []},
            "setup": {"folders": [], "services": []},
            "restore": {"folders": [], "services": []}}

def load_configs():
    if len(sys.argv) == 1:
        print "[!] Warning: No config file specified. Using default."
        if os.path.isfile("default.conf"):
            configfile.read("default.conf")
        else:
            return "[!] Error: default.conf not found. Exiting.."
    else:
        if os.path.isfile(sys.argv[1]):
            configfile.read(sys.argv[1])
        else:
            return "[!] Could not load config file", sys.argv[1]

    for section in configs:
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

        """Skip incompatible modules"""
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"):
            continue

        print "[+] Running", mod

        """If module is a service, retrieve additional args"""
        if prefix != "lin_" and prefix != "win_":
            if mod.split('_')[0] not in configs[mode]["services"]:
                continue
            try:
                mod_configs = configfile.items(mod.split('_')[0])
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
            result = sys.modules[mod].run(mod_configs)
        else:
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
    result = load_configs()
    if result:
        print result
        return

    while True:
        print "\n----- MENU -----"
        print "1) Install"
        print "2) Setup"
        print "3) Backup"
        print "4) Restore"
        print "5) Clean"
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
        elif choice == 0:
            return
        else:
            print "Invalid choice. Try again."

if __name__ == '__main__': main()
