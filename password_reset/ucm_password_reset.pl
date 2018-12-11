# ::Author:: ZhongYI (Charlie) Zhang at Cisco

use strict;
use warnings;

use Expect;
use IO::Socket::SSL;
use Term::ReadKey;

BEGIN { $ENV{PERL_LWP_SSL_VERIFY_HOSTNAME} = 0; }
BEGIN { IO::Socket::SSL::set_ctx_defaults( verify_mode => SSL_VERIFY_NONE); }

my $host = '';
my $username = '';
my $osOldPW = '';
my $osNewPW = '';

print "Enter the hostname for the server to reset password: ";
$host = <STDIN>; chomp $host;
print "Enter the username of the \"OS Administrator\": ";
$username = <STDIN>; chomp $username;
print "Enter the CURRENT password for \"OS Administrator\" user \"$username\": ";
ReadMode 'noecho';
$osOldPW = <STDIN>; chomp $osOldPW;
print "\nEnter the NEW password for \"OS Administrator\" user \"$username\": ";
$osNewPW = <STDIN>; chomp $osNewPW;
ReadMode 'original';
print "\n";

my $exp = new Expect;
$exp->raw_pty(0);
#	$exp->log_stdout(0);
#	$exp->debug(0);

my $command = "ssh $username\@$host";
$exp->spawn ($command) or die "Cannot spaw $command: $!\n";

# login
my $ucm_prompt = qr/admin: ?/;
my $timeout = 120;
my $rc = $exp->expect($timeout,
		[qr/continue connecting ?\(yes\/no\)\?/, sub {
														$exp->send("yes\r");
														exp_continue;
													}
		],
		[ qr/password: ?/, sub {
									$exp->send("$osOldPW\r");
									exp_continue;
								}
		],
		[$ucm_prompt,
		],
		);
if (!$rc)
	{
		$exp->hard_close();
		print "Failed to log into $host\n";
		exit;
	}

# change password
my $output = '';
my $sucessFlag = '';

my $cmd = "set password user admin\r";
$exp->send($cmd);
$rc = $exp->expect($timeout,
	[qr/Please enter the old password:/ => sub {
													$exp->send("$osOldPW\r");
													exp_continue;
												}
	],
	[qr/Please enter the new password:/i => sub {
													$exp->send("$osNewPW\r");
													exp_continue;
												}
	],
	[qr/Reenter new password to confirm:/i => sub {
													$exp->send("$osNewPW\r");
													exp_continue;
												}
	],
	[qr/Password updated successfully/i => sub {
													$sucessFlag = 1;
													exp_continue;
												}
	],
	[$ucm_prompt, sub { $output = $output.$exp->before();   $output =~ s/[\n|\r|\f]+/\n/mg; }
	],
);
if (!defined($rc)) { print "\nConnection broken, or timeout\n"; }
elsif ($sucessFlag) { print "\nUpdated OS Admin password successfully\n";}
else { print "$output\n";}

# close connection
$exp->send("exit\r");
$exp->hard_close();
print "\n";