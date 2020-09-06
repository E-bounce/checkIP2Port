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
