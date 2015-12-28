import ConfigParser, imp, os, sys

isWindows = True if (os.name == "nt") else False
configfile = ConfigParser.ConfigParser()
configfile.read("config")
configs = {"install": {"linux": [], "windows": [], "services": []},
            "backup": {"linux": [], "windows": [], "services": []},
            "setup": {"linux": [], "windows": [], "services": []},
            "restore": {"linux": [], "windows": [], "services": []}}

def backup():
    print ">>> Backup <<<"
    module_names = load_modules("backup")

    for mod in module_names:
        prefix = mod[:3]
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"): #Skip incompatible mods
            continue

        print "[+] Running", mod
        if prefix[-1] != '_': #Service = has additional args
            try:
                result = sys.modules[mod].run(configfile.items(mod))
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
        else:
            result = sys.modules[mod].run()

        if(result): #Display results
            print "[!] Error", result
        else:
            print "[*] Success!"

def clean():
    print ">>> Clean <<<"
    module_names = load_modules("Clean")

    for mod in module_names:
        prefix = mod[:3]
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"): #Skip incompatible mods
            continue

        print "[+] Running", mod
        if prefix[-1] != '_': #Service = has additional args
            try:
                result = sys.modules[mod].run(configfile.items(mod))
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
        else:
            result = sys.modules[mod].run()

        if(result): #Display results
            print "[!] Error", result
        else:
            print "[*] Success!"

def install():
    print ">>> Install <<<"
    module_names = load_modules("install")

    for mod in module_names:
        prefix = mod[:3]
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"): #Skip incompatible mods
            continue

        print "[+] Running", mod
        if prefix[-1] != '_': #Service = has additional args
            try:
                result = sys.modules[mod].run(configfile.items(mod))
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
        else:
            result = sys.modules[mod].run()

        if(result): #Display results
            print "[!] Error", result
        else:
            print "[*] Success!"

def load_configs():
    for section in configs:
        try:
            configs[section]["linux"] = configfile.get(section, "linux").split(",")
        except:
            print "[?] No Linux variable in", section

        try:
            configs[section]["windows"] = configfile.get(section, "windows").split(",")
        except:
            print "[?] No Windows variable in", section

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

def restore():
    print ">>> Restore <<<"
    module_names = load_modules("restore")

    for mod in module_names:
        prefix = mod[:3]
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"): #Skip incompatible mods
            continue

        print "[+] Running", mod
        if prefix[-1] != '_': #Service = has additional args
            try:
                result = sys.modules[mod].run(configfile.items(mod))
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
        else:
            result = sys.modules[mod].run()

        if(result): #Display results
            print "[!] Error", result
        else:
            print "[*] Success!"

def setup():
    print ">>> Set Up <<<"
    module_names = load_modules("setup")

    for mod in module_names:
        prefix = mod[:3]
        if (isWindows and prefix == "lin_") or (not isWindows and prefix == "win_"): #Skip incompatible mods
            continue

        print "[+] Running", mod
        if prefix[-1] != '_': #Service = has additional args
            try:
                result = sys.modules[mod].run(configfile.items(mod))
            except: #Error if no service section
                print "[!] Insufficient config options provided for", mod
                return
        else:
            result = sys.modules[mod].run()

        if(result): #Display results
            print "[!] Error", result
        else:
            print "[*] Success!"

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
    load_configs()

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
            install()
        elif choice == 2:
            setup()
        elif choice == 3:
            backup()
        elif choice == 4:
            restore()
        elif choice == 5:
            clean()
        elif choice == 0:
            return
        else:
            print "Invalid choice. Try again."

if __name__ == '__main__': main()
