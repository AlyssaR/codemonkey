import datetime, os, platform, sys, zipfile

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """

    if not os.path.isdir("archive"): #create archive directory if it doesn't exist
        os.makedirs("archive")

    zip_name = datetime.datetime.now().strftime("archive/" + platform.node() + "_%Y-%m-%d_%H-%M.zip")
    with zipfile.ZipFile(zip_name, "w") as zip_file:
        for thing in args:
            if os.path.isdir(thing):
                for root, dirs, files in os.walk(thing):
                    for f in files:
                        zip_file.write(os.path.join(root, f))
            else:
                zip_file.write(thing)

    print "[+] Added all files and directories to archive."
    return

def main():
    print "[+] Testing Folder Backup"
    run(sys.argv[1:])

if __name__ == '__main__': main()
