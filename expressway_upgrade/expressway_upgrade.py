"""
:author: Graham White
"""
import subprocess
import time
import getpass


def do_backup(server, password):
    cmd = 'sshpass -p {} ssh -o StrictHostKeyChecking=no root@{} "echo random_key | /sbin/backup.sh"'.format(password, server)
    exitcode, data = subprocess.getstatusoutput(cmd)
    return exitcode, data


def do_install(server, image, password):
    sleeptime, waittime = 60, 6000

    cmd = 'sshpass -p {} scp -o StrictHostKeyChecking=no {} root@{}:/tmp/tandberg-image.tar.gz'.format(password, image, server)
    starttime = time.time()
    exitcode, data = subprocess.getstatusoutput(cmd)
    if exitcode:
        return False
    else:
        time.sleep(20)

    cmd = 'sshpass -p {} ssh -o StrictHostKeyChecking=no root@{} "ls -l /tmp/install*"'.format(password, server)
    while time.time() - starttime < waittime:
        exitcode, data = subprocess.getstatusoutput(cmd)
        if 'No such file or directory' in data:
            return 'FAILED: {}\n{}'.format(server,data)
        if 'install-ok' in data:
            return 'install-ok for server {}'.format(server)
    time.sleep(sleeptime)

    return 'TIMEOUT: {}\n{}'.format(server,data)


def tshell_reboot(server, password):
    cmd = 'sshpass -p {} ssh -o StrictHostKeyChecking=no root@{} "echo xCommand Boot | tshell"'.format(password, server)
    exitcode, data = subprocess.getstatusoutput(cmd)
    print(data)
    if exitcode or 'OK' not in data:
        return False
    return True


if __name__ == '__main__':
    # get hostname and root password
    print("What expressway server do you want to upgrade?")
    host = input('Hostname or IP: ')
    print("We need root access for upgrades")
    root_pass = getpass.getpass('root password: ')

    # do backup
    print("starting backup")
    exitcode, data = do_backup(host, root_pass)
    print(exitcode)
    print(data)

    # copy over image and install
    print("\nfilename of the image to upgrade to (must be in folder 'images')")
    image_filename = input('filename: ')

    print("starting to copy image, this may take a while ...")
    res = do_install(host, 'images/' + image_filename, root_pass)
    print(res)

    # reboot
    if tshell_reboot(host, root_pass):
        print('rebooting ... ')
    else:
        print('reboot command failed')
