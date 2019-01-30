### required: folder /images
this would be the folder where the script will be looking for and image file

### required: sshpass (UX)
In the script, sshpass is used for SSH with simple password authentication.   
This is for testing purposes, in production you should probably use passwordless  
ssh using trusted keys  
see the [Expressway Admin Guide](https://www.cisco.com/c/dam/en/us/td/docs/voice_ip_comm/expressway/admin_guide/Cisco-Expressway-Administrator-Guide-X8-10.pdf) for details

### sample output
```
$ python3 expressway_upgrade.py
What expressway server do you want to upgrade?
Hostname or IP: svluc-******
We need root access for upgrades
root password:
starting backup
0
SVL-UCV LAB VCS Cluster
Please contact svl-u*****@cisco.com to report any issues with this application


Starting backup...
Backup complete: /mnt/harddisk/backuprestore/system_backup/X8.11.4_02942F39_2019_01_29__07_39_44_backup.tar.gz.enc

filename of the image to upgrade to(must be in folder 'images')
filename: s42700x8_11_4.tar.gz
starting to copy image, this may take a while ...
install-ok for server svluc******
rebooting ...
```