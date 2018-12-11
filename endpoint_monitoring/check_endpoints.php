<?php

// First get a list of room devices
include_once('axl.class.php');

$TELEPRESENCE_EXCLUDE_DX = '
	select device.name as devicename, device.name as mac, device.description as description, typemodel.name as model, numplan.dnorpattern as dirnumber, device.specialloadinformation as configured_load from device
	join devicenumplanmap on devicenumplanmap.fkdevice=device.pkid
	join numplan on devicenumplanmap.fknumplan=numplan.pkid
	join typemodel on device.tkmodel=typemodel.enum
	where device.tkclass = "1"
	and device.name like "SEP%"
	and (typemodel.name like "Cisco TelePresence %" or typemodel.name like "Cisco Spark Room %" or typemodel.name like "Cisco Webex Room %")
	and typemodel.name != "Cisco TelePresence DX70" and typemodel.name != "Cisco TelePresence DX80"
	order by device.description
';

$_axl = new axl('username', 'password', 'server.corp.com');
$_result = $_axl->doRequest('ExecuteSQLQuery', array('sql' => $TELEPRESENCE_EXCLUDE_DX));

print_r($_result);

// Go over the list and connect to every device checking for errors
foreach($_result->return->row as $device) {
    // print($device->devicename . "\n");

}
?>
