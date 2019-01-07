<?php
class RIS
{
   	function __construct($user, $pwd, $server) {
    	$this->user = $user;
	    $this->pwd = $pwd;
	    $this->server = $server;
		$this->setClient();
	}

	private function setClient() {
        $context = stream_context_create([
       	    'ssl' => [
       	        # set some SSL/TLS specific options, not for production
       	        'verify_peer' => false,
       	        'verify_peer_name' => false,
       	        'allow_self_signed' => true
       	    ]
        ]);

        # Create SOAP Connection
        $this->soap_ris = new SoapClient(__DIR__ . "/schema/RisPort70.wsdl",
    	    array(
    		    'trace'=>true,
    		    'exceptions'=>true,
    		    'location'=>"https://".$this->server.":8443/realtimeservice2/services/RISService70",
    		    'login'=>$this->user,
    		    'password'=>$this->pwd,
    		    'stream_context' => $context
    	    ));
    }

    public function get_IP($devices_list) {
        # Create body
        $xmlBody =
        	'<ns1:selectCmDeviceExt>
        	<ns1:StateInfo></ns1:StateInfo>
        	<ns1:CmSelectionCriteria>
        	<ns1:MaxReturnedDevices>1000</ns1:MaxReturnedDevices>
        	<ns1:DeviceClass>Any</ns1:DeviceClass>
        	<ns1:Model></ns1:Model>
        	<ns1:Status>Registered</ns1:Status>
        	<ns1:NodeName></ns1:NodeName>
        	<ns1:SelectBy>Name</ns1:SelectBy>
        	<ns1:SelectItems>';

        foreach($devices_list as $device)
        	$xmlBody .= '<ns1:item><ns1:Item>'.$device->devicename.'</ns1:Item></ns1:item>';
        $xmlBody .=
        	'</ns1:SelectItems>
        	<ns1:Protocol>Any</ns1:Protocol>
        	<ns1:DownloadStatus>Any</ns1:DownloadStatus>
        	</ns1:CmSelectionCriteria>
        	</ns1:selectCmDeviceExt>';

        print($xmlBody);
        $soapBody = new SoapVar($xmlBody, XSD_ANYXML);

        $response = $this->soap_ris->selectCmDeviceExt($soapBody);
        print_r($response);

        $device_ip = array();
        foreach($response->selectCmDeviceReturn->SelectCmDeviceResult->CmNodes->item as $server)
        {
            if ($server->ReturnCode == "Ok")
            // $server->CmDevices->item will be a stdClass if only 1 device
            // it will be an array of stdClass if multiple devices are
            // found on that server
            {
                if (! is_array($server->CmDevices->item))
                {
                    print($server->CmDevices->item->Name . "\n");
                    print($server->CmDevices->item->IPAddress->item->IP . "\n");
                    $device_ip[$server->CmDevices->item->Name] =
                        $server->CmDevices->item->IPAddress->item->IP;
                }
                else
                {
                    foreach($server->CmDevices->item as $device)
                    {
                        print($device->Name . "\n");
                        print($device->IPAddress->item->IP . "\n");
                        $device_ip[$device->Name] =
                            $device->IPAddress->item->IP;
                    }
                }
            }
        }
        return $device_ip;
    }
}
?>