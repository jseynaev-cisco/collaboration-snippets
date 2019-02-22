this script will get a list of MX200 devices from the UCM, query the UCM 
again to find the IP addresses of all devices.  
After that, it will contact each device and query for the Touchpanel 
status

#### required: folder /schema
This contains the AXL SOAP wsdl files and can be downloaded from any UCM server.

Go to "Application > Plugins"  
From that page download the "AXL Toolkit"

Unzip the file and a folder called "schema" should be present, copy that whole folder in here for the axl class to work

#### required: php-soap
soap library for PHP, install as per your OS/environment  
e.g. `apt-get install php-soap` for Ubuntu

#### required: php-curl
soap library for PHP, install as per your OS/environment  
e.g. `apt-get install php-curl` for Ubuntu

#### Sample output
```
# php check_endpoints.php
server to connect to (AXL must be running): ucm-e*****
username with AXL permissions: jse******
Password:
stdClass Object
(
    [return] => stdClass Object
        (
            [row] => Array
                (
                    [0] => stdClass Object
                        (
                            [devicename] => SEP005*******
                            [model] => Cisco TelePresence MX200
                        )

                    [1] => stdClass Object
                        (
                            [devicename] => SEPD86**********
                            [model] => Cisco TelePresence MX200
                        )

                    [2] => stdClass Object
                        (

						[...]
						
                )

        )

)
<ns1:selectCmDeviceExt>
                <ns1:StateInfo></ns1:StateInfo>
                <ns1:CmSelectionCriteria>
                <ns1:MaxReturnedDevices>1000</ns1:MaxReturnedDevices>
                <ns1:DeviceClass>Any</ns1:DeviceClass>
                <ns1:Model></ns1:Model>
                <ns1:Status>Registered</ns1:Status>
                <ns1:NodeName></ns1:NodeName>
                <ns1:SelectBy>Name</ns1:SelectBy>
                <ns1:SelectItems><ns1:item><ns1:Item>SEP00**********</ns1:Item></ns1:item><ns1:item><ns1:Item>SEPD8*********</ns1:Item></ns1:item>[...]</ns1:SelectItems>
                <ns1:Protocol>Any</ns1:Protocol>
                <ns1:DownloadStatus>Any</ns1:DownloadStatus>
                </ns1:CmSelectionCriteria>
                </ns1:selectCmDeviceExt>stdClass Object
(
    [selectCmDeviceReturn] => stdClass Object
        (
            [SelectCmDeviceResult] => stdClass Object
                (
                    [TotalDevicesFound] => 78
                    [CmNodes] => stdClass Object
                        (
                            [item] => Array
                                (
                                    [0] => stdClass Object
                                        (
                                            [ReturnCode] => NotFound
                                            [Name] => ucm-e*****
                                            [NoChange] => 1
                                            [CmDevices] =>
                                        )

                                    [1] => stdClass Object
                                        (
                                            [ReturnCode] => NotFound
                                            [Name] => ucm-e****
                                            [NoChange] => 1
                                            [CmDevices] =>
                                        )

                                    [2] => stdClass Object
                                        (
                                            [ReturnCode] => NotFound
                                            [Name] => ucm-e******
                                            [NoChange] => 1
                                            [CmDevices] =>
                                        )

                                    [3] => stdClass Object
                                        (
                                            [ReturnCode] => Ok
                                            [Name] => ucm-e******
                                            [NoChange] =>
                                            [CmDevices] => stdClass Object
                                                (
                                                    [item] => Array
                                                        (
                                                            [0] => stdClass Object
                                                                (
                                                                    [Name] => SEPD86********
                                                                    [DirNumber] => +254202**-Registered
                                                                    [DeviceClass] => Phone
                                                                    [Model] => 617
                                                                    [Product] => 0
                                                                    [BoxProduct] => 0
                                                                    [Httpd] => Yes
                                                                    [RegistrationAttempts] => 0
                                                                    [IsCtiControllable] => 1
                                                                    [LoginUserId] =>
                                                                    [Status] => Registered
                                                                    [StatusReason] => 0
                                                                    [PerfMonObject] => 2
                                                                    [DChannel] => 0
                                                                    [Description] => MOUNT KILIMANJARO (4) Video (1-Screen)(Public)
                                                                    [H323Trunk] => stdClass Object
                                                                        (
                                                                            [ConfigName] =>
                                                                            [TechPrefix] =>
                                                                            [Zone] =>
                                                                            [RemoteCmServer1] =>
                                                                            [RemoteCmServer2] =>
                                                                            [RemoteCmServer3] =>
                                                                            [AltGkList] =>
                                                                            [ActiveGk] =>
                                                                            [CallSignalAddr] =>
                                                                            [RasAddr] =>
                                                                        )

                                                                    [TimeStamp] => 1547903169
                                                                    [Protocol] => SIP
                                                                    [NumOfLines] => 1
                                                                    [LinesStatus] => stdClass Object
                                                                        (
                                                                            [item] => stdClass Object
                                                                                (
                                                                                    [DirectoryNumber] => +25420*
                                                                                    [Status] => Registered
                                                                                )

                                                                        )

                                                                    [ActiveLoadID] => TC7.3.15.a9f4c3a
                                                                    [InactiveLoadID] =>
                                                                    [DownloadStatus] => Unknown
                                                                    [DownloadFailureReason] =>
                                                                    [DownloadServer] =>
                                                                    [IPAddress] => stdClass Object
                                                                        (
                                                                            [item] => stdClass Object
                                                                                (
                                                                                    [IP] => 10.229.207.21
                                                                                    [IPAddrType] => ipv4
                                                                                    [Attribute] => Unknown
                                                                                )

                                                                        )

                                                                )

                                                            [1] => stdClass Object
                                                                (

																[...]
																
SEPD86**********
10.229.207.21
SEP00**********
10.228.22.76
[...]
Array
(
    [SEPD86**********] => 10.229.207.21
    [SEP00***********] => 10.228.22.76
	[...]
)
username with admin permissions on devices: admin
Password:
SEP00**********: Touchpanel found
SEP00**********: not registered (no IP)
SEP00**********: Touchpanel not found
[...]
```