def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    print ", ".join(args)


def main():
    run(["blah", "blah"])

if __name__ == '__main__': main()
