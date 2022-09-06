# idracup.py
A simple CLI script to start or stop your Dell PowerEdge with iDRAC

Simplify your CLI interaction with your Dell PowerEdge R720's iDRAC.
Quickly send a boot or shutdown command with this Python script.
The script will establish an SSH channel via which you send your command.

Please note: if you have a hypervisor running on your server, it is generally
better to shutdown the server via the hypervisor. If the hypervisor is unresponsive
or not installed, you can use this script to shut down the server.

If you have issues running the script, be sure to install the requirements from requirements.txt

For more information on iDRAC CLI commands, 
see: https://cs.uwaterloo.ca/~brecht/servers/docs/PowerEdge-2600/en/Racadm/racadmc1.htm

    Usage:      python idracup.py [HOST] [COMMAND] [OPTION]
    Example:    python idracup.py i- 192.168.1.100 -s  

    You will be prompted for the iDRAC password after entering the command
    
    Commands:
    -s, --startup           issue the startup command
    -d, --shutdown          issue the shutdown command

    Options:
    -h, --help              this help menu
    -u, --user=USERNAME     login with a user other than root
