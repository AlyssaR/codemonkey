def run():
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    print "Received input of:",
    for a in args:
        print ">", a

    if len(args) < 2:
        return "Not enough arguments"
    else:
        return

def main():
    print "Testing system"
    result = run()
    if not result:
        print "Collected System Profile"
    else:
        print "[!] Error", result

if __name__ == '__main__': main()
