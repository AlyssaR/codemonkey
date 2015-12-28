def run(args):
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
