import os, subprocess

def run(args):
    """
    INPUT:  args        List of arguments, may be a list of objects
    OUTPUT:             If success, just use a plain return
            string      If error, return string error message
    """
    print "Installing Elk"

    #1) Create user for elk

    """Edit config files with ip address"""
    ip = [x[1] for x in args if x[0] == "localip"][0]
    with open("./resources/elk/docker_compose.yml", "a") as compose_file:
        compose_file.write("\t\tELASTICSEARCH_URL: http://" + ip + ":9200")
    with open("./resources/elk/logstash/logstash.conf", "a") as logstash_file:
        logstash_file.write("output {\n\telasticsearch {\n\t\thosts => [\"" + ip + "\"]\n\t}\n}")

    #4) Compose
    #5) Security things?
    return
