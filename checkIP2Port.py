import requests
import sys
import getopt
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}


def usage():
    print(r"""
       _               _    _____ _____ ___  _____           _   
      | |             | |  |_   _|  __ \__ \|  __ \         | |  
   ___| |__   ___  ___| | __ | | | |__) | ) | |__) |__  _ __| |_ 
  / __| '_ \ / _ \/ __| |/ / | | |  ___/ / /|  ___/ _ \| '__| __|
 | (__| | | |  __/ (__|   < _| |_| |    / /_| |  | (_) | |  | |_ 
  \___|_| |_|\___|\___|_|\_\_____|_|   |____|_|   \___/|_|   \__|
                                                                 
    >>>>>>>>>>
     By Ebounce
     A simple tool to check the result of scaning ip by nmap or masscan;
     you can use 4 modes below
     user-help:
     one2one mode example: python3 checkIP2Port.py -i 1.1.1.1 -p 80
     one2more mode example: python3 checkIP2Port.py -i 1.1.1.1 -pF=<portFile>
     more2one mode example: python3 checkIP2Port.py -iF=<ipFile> -p 80
     more2more mode example: python3 checkIP2Port.py -iF=<ipFile> -pF=<portFile>
     Example:
     python3 checkIP2Port.py -ip 1.1.1.1 -pF=./portList.txt
     python3 checkIP2Port.py -iF=./ipList.txt -pF=./portList.txt
     >>>>>>>>>>
    """
          )


def one2one(ip, port):
    resp = requests.get("http://" + ip + ":" + port, headers=header, timeout=1.5)
    parser = BeautifulSoup(resp.text, "html.parser")
    if parser.title is not None:
        return print(
            "Result: Address: {} Code: {} title: {}".format(ip + ":" + port, resp.status_code, parser.title.string))
    else:
        return print("Result: Address: {} Code: {} ".format(ip + ":" + port, resp.status_code))


def one2more(ip, portFile):
    with open(portFile, "r") as portTxt:
        for port in portTxt.read().split("\n"):
            try:
                one2one(ip, port)
            except Exception as e:
                print("Result: Address: {} Error: ".format(ip + ":" + port), end="")
                print(e)
        portTxt.close()
    return


def more2one(ipFile, port):
    with open(ipFile, "r") as ipTxt:
        for ip in ipTxt.read().split("\n"):
            one2one(ip, port)
        ipTxt.close()
    return


def more2more(ipFile, portFile):
    ipTxt = open(ipFile, "r")
    portTxt = open(portFile, "r")
    for ip in ipTxt.read().split("\n"):
        for port in portTxt.read().split("\n"):
            one2one(ip, port)
    return


def parseParam2Execute():
    ip = ""
    port = ""
    ipFile = ""
    portFile = ""
    opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ['help', 'pF=', 'iF='])
    if len(opts) != 2:
        usage()
        sys.exit()
    for op, arg in opts:
        if op == "-i":
            ip = arg
        if op == "-p":
            port = arg
        if op == "-iF":
            ipFile = arg
        if op == "--pF":
            portFile = arg
        if op in ("-h", "--help"):
            usage()
            sys.exit()
    usage()
    if ip != "" and port != "":
        one2one(ip, port)
        return
    elif ipFile != "" and port != "":
        more2one(ipFile, port)
        return
    elif ip != "" and portFile != "":
        one2more(ip, portFile)
        return
    elif ipFile != "" and portFile != "":
        more2more(ipFile, portFile)
        return


if __name__ == "__main__":
    parseParam2Execute()
