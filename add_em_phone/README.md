This example will add an extension mobility enabled phone to the unified 
communications manager with only the bare minimum (required) settings.  

It will ask for all information needed, which is quite a bit. In real life 
situations most of the info can probably be derived from a couple of datapoints 
combined with a proper standard, e.g. if you have the sitename, the line css, 
phone css and devices pool could have a standard naming of "\<site\> Emergency", 
"\<site\> Restricted" and "\<site\> em phones".  
Based on the site, you might also be able to get the 'next available number'
either from UCM or from a telephony number management system

### sample output
This one is a bit elaborate, but is shows the output one gets from both the 
AXL and the RIS calls

```
$ python3 add_em_phone.py
ucm server and user with UCM AXL privileges
ucm hostname or IP: ucm-e******
username: jsey*****
password:
We'll need a couple of details on the phone (9971)
MAC (SEP will be prefixed): AAAABBBBCCCC
Calling Search Space for the phone: KJK Local
Partition for the line: CORE 8Digit
Calling Search Space for the line: KJK Local
Device Pool: KJK Phones AMS151-BRU152
Number / DN: 83250003
Reception or central number (for a speeddial): 444
<line>
    <pattern>83250003</pattern>
    <description>Logged 0ff EM - TEST CL 2019</description>
    <usage>Device</usage>
    <routePartitionName>CORE 8Digit</routePartitionName>
    <alertingName>Logged 0ff EM</alertingName>
    <asciiAlertingName>Logged 0ff EM</asciiAlertingName>
    <shareLineAppearanceCssName>KJK Local</shareLineAppearanceCssName>
</line>
<phone>
    <name>SEPAAAABBBBCCCC</name>
    <description>Logged off EM</description>
    <product>Cisco 9971</product>
    <model>Cisco 9971</model>
    <class>Phone</class>
    <protocol>SIP</protocol>
    <protocolSide>User</protocolSide>
    <callingSearchSpaceName>KJK Local</callingSearchSpaceName>
    <devicePoolName>KJK Phones AMS151-BRU152</devicePoolName>
    <commonDeviceConfigName>Cisco-User</commonDeviceConfigName>
    <commonPhoneConfigName>Standard Common Phone Profile</commonPhoneConfigName>
    <networkLocation>Use System Default</networkLocation>
    <securityProfileName>Cisco 9971 - Standard SIP Non-Secure Profile</securityProfileName>
    <sipProfileName>Standard SIP Profile</sipProfileName>
    <lines>
        <line>
            <index>1</index>
            <dirn>
                <pattern>83250003</pattern>
                <routePartitionName>CORE 8Digit</routePartitionName>
            </dirn>
        </line>
    </lines>
    <phoneTemplateName>Standard 9971 SIP</phoneTemplateName>
    <speeddials>
        <speeddial>
            <dirn>8888</dirn>
            <label>Helpdesk</label>
            <index>1</index>
        </speeddial>
        <speeddial>
            <dirn>444</dirn>
            <label>Reception</label>
            <index>2</index>
        </speeddial>
    </speeddials>
    <enableExtensionMobility>true</enableExtensionMobility>
    <allowCtiControlFlag>true</allowCtiControlFlag>
</phone>
adding new line
OrderedDict([('return', '{4B4A5B2A-8020-4242-EA85-B29C6BFCB1A6}')])
adding new phone
OrderedDict([('return', '{1ACB30BB-B44E-04BA-734D-00DED5FD6F37}')])
$
```