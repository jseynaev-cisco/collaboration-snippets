<?php

// First get a list of room devices
include_once('axl.class.php');

$TELEPRESENCE_EXCLUDE_DX = '
	select device.name as devicename, typemodel.name as model from device
	join typemodel on device.tkmodel=typemodel.enum
	and typemodel.name like "Cisco TelePresence MX200%"
';

// Ask a few things
$server = readline('server to connect to (AXL must be running): ');
$username = readline('username with AXL permissions: ');
$password = readline('password: ');


$_axl = new axl($username, $password, $server);
$_result = $_axl->doRequest('ExecuteSQLQuery', array('sql' => $TELEPRESENCE_EXCLUDE_DX));

// Go over the list and get IP from RIS
foreach($_result->return->row as $device) {
    print_r($device);
}

// Go over the list and connect to every device checking for errors on touch
$issues = array();
foreach($_result->return->row as $device) {
    // print($device->devicename . "\n");
}

$ip = "10.229.54.64";
$username = readline('username with admin permissions on devices: ');
$password = readline('password: ');

$_ch = curl_init();
curl_setopt($_ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($_ch, CURLOPT_CONNECTTIMEOUT, 10);
curl_setopt($_ch, CURLOPT_TIMEOUT, 10);

curl_setopt($_ch, CURLOPT_URL, "https://".$ip."/putxml");
curl_setopt($_ch, CURLOPT_POST, 1);
curl_setopt($_ch, CURLOPT_POSTFIELDS, "<Command><Peripherals><List><Type>TouchPanel</Type><Connected>True</Connected></List></Peripherals></Command>");

$_token = base64_encode($username.':'.$password);
$_header = array(
	'Content-Type: text/xml',
	'Authorization: Basic '.$_token,
	);
curl_setopt($_ch, CURLOPT_HTTPHEADER, $_header);
curl_setopt($_ch, CURLOPT_SSL_VERIFYPEER, 0);
curl_setopt($_ch, CURLOPT_SSL_VERIFYHOST, 0);
curl_setopt($_ch, CURLOPT_HEADER, 0);
curl_setopt($_ch, CURLOPT_VERBOSE, 0);

$_rep = curl_exec($_ch);
var_dump($_rep);
if( ! isset($_ch) )
    curl_close($_ch);


// Create ticket for issues
// Not sure how far we can go here, obviously we won't create anything


?>



