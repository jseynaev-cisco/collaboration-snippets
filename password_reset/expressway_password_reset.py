"""
:author: Stephen Greszczyszyn at Cisco
"""

import getpass
import paramiko

# get hostname and root password
print("What expressway server do you want to change a password on?")
host = input('Hostname or IP: ')
print("We need root access for changing passwords")
root_pass = getpass.getpass('Current root password: ')

# get username for who to change the password as well as the new password
user = input("Please enter username for password change: ")
new_pass = getpass.getpass('New password for {}: '.format(user))
new_pass2 = getpass.getpass('Please enter new password again: ')
if new_pass != new_pass2:
    print("passwords don't match")
    exit(1)

# Initialise SSH login, make sure to auto accept new keys
with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # don't do this in production
    try:
        ssh.connect(host, username="root", password=root_pass, timeout=5, look_for_keys=False)
    except Exception as message:
        print('Could not login to host {}: {}'.format(host, str(message)))
        raise

    # we're logged in, change password
    stdin, stdout, stderr = ssh.exec_command('passwd {}'.format(user))
    stdin.write(new_pass+"\n")
    stdin.flush()
    stdin.write(new_pass+"\n")
    stdin.flush()
    exit_status = stdout.channel.recv_exit_status()

    if exit_status == 0:
        print('password changed successfully for {}'.format(user))
    else:
        print('issue while trying to change password for {}'.format(user))

