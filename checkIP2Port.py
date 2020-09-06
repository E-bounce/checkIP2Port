import requests
import sys
import getopt
from bs4 import BeautifulSoup
import re

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
}


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
     param help:
     --mass= parse the file created by "masscan -oG"
     -i target ip
     -p target port
     -iF target ip file
     -pF target port file
     -v very detailed output
     -s use https
     user-help:
     one2one mode example: python3 checkIP2Port.py -i 1.1.1.1 -p 80
     one2more mode example: python3 checkIP2Port.py -i 1.1.1.1 -pF=<portFile>
     more2one mode example: python3 checkIP2Port.py -iF=<ipFile> -p 80
     more2more mode example: python3 checkIP2Port.py -iF=<ipFile> -pF=<portFile>
     masscan -oG result file : python3 checkIP2Port.py --mass=<result film>
     Example:
     python3 checkIP2Port.py -ip 1.1.1.1 -pF=./portList.txt
     python3 checkIP2Port.py -iF=./ipList.txt -pF=./portList.txt
     python3 checkIP2Port.py --mass=./result.txt -v
     >>>>>>>>>>
    """
          )


def load(filename):
    with open(filename, "r") as file:
        dataList = file.read().split("\n")
        file.close()
    return dataList[2:len(dataList)]


def parseMasscan(filename, isHttps, detail):
    datalist = load(filename)
    r_ip = re.compile(r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{'
                      r'2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|['
                      r'1-9]\d{1,3}|[0-9]))')
    for line in datalist:
        temp_address = r_ip.findall(line)
        try:
            if len(temp_address):
                one2one(temp_address[0][0], temp_address[0][1], isHttps)
        except Exception as e:
            if not detail:
                continue
            print("Result: Address: {} Error: ".format(temp_address[0][0] + ":" + temp_address[0][1]), end="")
            print(e)


def one2one(ip, port, isHttps):
    if isHttps:
        resp = requests.get("https://" + ip + ":" + port, headers=header, timeout=1.5)
        print(resp.text)
    else:
        resp = requests.get("http://" + ip + ":" + port, headers=header, timeout=1.5)
    parser = BeautifulSoup(resp.text, "html.parser")
    if parser.title is not None:
        return print(
            "Result: Address: {} Code: {} title: {}".format(ip + ":" + port, resp.status_code, parser.title.string))
    else:
        return print("Result: Address: {} Code: {} ".format(ip + ":" + port, resp.status_code))


def one2more(ip, portFile, isHttps, detail):
    with open(portFile, "r") as portTxt:
        for port in portTxt.read().split("\n"):
            try:
                one2one(ip, port, isHttps)
            except Exception as e:
                if not detail:
                    continue
                print("Result: Address: {} Error: ".format(ip + ":" + port), end="")
                print(e)
        portTxt.close()
    return


def more2one(ipFile, port, isHttps, detail):
    ipTxt = open(ipFile, "r")
    for ip in ipTxt.read().split("\n"):
        try:
            one2one(ip, port, isHttps)
        except Exception as e:
            if not detail:
                continue
            print("Result: Address: {} Error: ".format(ip + ":" + port), end="")
            print(e)
        ipTxt.close()
    return


def more2more(ipFile, portFile, isHttps, detail):
    ipTxt = open(ipFile, "r")
    portTxt = open(portFile, "r")
    for ip in ipTxt.read().split("\n"):
        for port in portTxt.read().split("\n"):
            try:
                one2one(ip, port, isHttps)
            except Exception as e:
                if not detail:
                    continue
                print("Result: Address: {} Error: ".format(ip + ":" + port), end="")
                print(e)
    ipTxt.close()
    portTxt.close()
    return


def parseParam2Execute():
    ip = ""
    port = ""
    ipFile = ""
    portFile = ""
    filename = ""
    detail = False
    isHttps = False
    isMass = False
    opts, args = getopt.getopt(sys.argv[1:], "hi:p:sv", ['help', 'pF=', 'iF=', 'mass='])
    usage()
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
        if op == "-s":
            isHttps = True
        else:
            isHttps = False
        if op == "-v":
            detail = True
        else:
            detail = False
        if op == "--mass":
            filename = arg
            isMass = True
    if ip != "" and port != "":
        one2one(ip, port, isHttps)
        return
    elif ipFile != "" and port != "":
        more2one(ipFile, port, isHttps, detail)
        return
    elif ip != "" and portFile != "":
        one2more(ip, portFile, isHttps, detail)
        return
    elif ipFile != "" and portFile != "":
        more2more(ipFile, portFile, isHttps, detail)
        return
    elif isMass:
        parseMasscan(filename, isHttps, detail)


if __name__ == "__main__":
    parseParam2Execute()
