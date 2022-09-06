import argparse
from getpass_asterisk.getpass_asterisk import getpass_asterisk
import paramiko


'''
Simplify your CLI interaction with your Dell PowerEdge R720's iDRAC.
Quickly send a boot or shutdown command with this Python script.
The script will establish an SSH channel via which you send your command.

If you have issues running the script, be sure to install the requirements from requirements.txt

For more information on iDRAC CLI commands, 
see: https://cs.uwaterloo.ca/~brecht/servers/docs/PowerEdge-2600/en/Racadm/racadmc1.htm
'''


def help_menu():
    print('''
    Usage:      python idracup.py [HOST] [COMMAND] [OPTION]
    Example:    python idracup.py i- 192.168.1.100 -s  

    You will be prompted for the iDRAC password after entering the command
    
    Commands:
    -s, --startup           issue the startup command
    -d, --shutdown          issue the shutdown command

    Options:
    -h, --help              this help menu
    -u, --user=USERNAME     login with a user other than root
    ''')


def usage():
    print('''
    Usage:      python idracup.py [HOST] [COMMAND] [OPTION]
    Example:    python idracup.py -i 192.168.1.100 -s 
    Try --help for the full list of commands
    ''')


def ssh_connect(idrac_ip, uname, pword, cmd):
    print(f'[*] ESTABLISHING CONNECTION WITH {idrac_ip}')
    try:
        transport = paramiko.Transport(idrac_ip)
        transport.connect(username=uname)
        transport.auth_password(uname, pword)
        transport.auth_interactive_dumb(uname)
        channel = transport.open_session()
        channel.exec_command(cmd)
        print('[*] CONNECTION ESTABLISHED')
        print('[*] SENDING COMMAND')
        response = channel.recv(1024).decode('utf-8').strip()
        print(f'[*] COMMAND RECEIVED - iDRAC RESPONSE: {response}')
        print('[*] TERMINATING CONNECTION')
        channel.close()
        print('[*] CONNECTION CLOSED')
    except paramiko.ssh_exception.AuthenticationException:
        print('[!] INVALID PASSWORD OR USERNAME')
    except paramiko.ssh_exception.SSHException:
        print('[!] UNABLE TO ESTABLISH A CONNECTION - HOST NOT UP OR INVALID ADDRESS')


def main():
    parser = argparse.ArgumentParser(prog='idracup.py',
                                     usage='python %(prog)s [option] [option]')
    parser.add_argument('-i', '--ipaddress', action='store', dest='ip_address', required=True,
                        help='the ip address of your iDRAC controller')
    parser.add_argument('-u', '--username', action='store', default='root', dest='username',
                        help='login with another user other than root, which is default')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--startup', action='store_true', dest='startup',
                       help='issue the iDRAC startup command')
    group.add_argument('-d', '--shutdown', action='store_true', dest='shutdown',
                       help='issue the iDRAC shutdown command')
    args = parser.parse_args()

    pword = getpass_asterisk(prompt='Enter iDRAC password: ')
    idrac_ip = args.ip_address
    uname = args.username

    if args.startup:
        cmd = 'racadm serveraction powerup'
        ssh_connect(idrac_ip, uname, pword, cmd)

    elif args.shutdown:
        cmd = 'racadm serveraction powerdown'
        ssh_connect(idrac_ip, uname, pword, cmd)


if __name__ == '__main__':
    main()
