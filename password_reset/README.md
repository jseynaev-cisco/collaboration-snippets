These two scripts will automate changing passwords, on for the expressway and 
another for the UCM platform  
We're using Paramiko in Python and Expect module in Perl to run the 'passwd'
and 'set password user' cli commands

#### sample output
```bash
# python3 expressway_password_reset.py
What expressway server do you want to change a password on?
Hostname or IP: svl*****
We need root access for changing passwords
Current root password:
Please enter username for who to change the password: admin
New password for admin:
Please enter new password again:
password changed successfully for admin
#
```

```bash
# perl ucm_password_reset.pl
Enter the hostname for the server to reset password: svl******
Enter the username of the "OS Administrator": ucadmin
Enter the CURRENT password for "OS Administrator" user "ucadmin":
Enter the NEW password for "OS Administrator" user "ucadmin":
ucadmin@svluc-ucm-111's password:
Command Line Interface is starting up, please wait ...

   Welcome to the Platform Command Line Interface

VMware Installation:
        2 vCPU: Intel(R) Xeon(R) CPU E5-2690 v4 @ 2.60GHz
        Disk 1: 110GB, Partitions aligned
        8192 Mbytes RAM

admin:set password user admin
Please enter the old password: ************
   Please enter the new password: ********
Reenter new password to confirm: ********
Please wait...


Password updated successfully.
admin:
Updated OS Admin password successfully
#
```