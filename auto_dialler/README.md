this auto-dialler uses the linphone softphone to make a call.  
The script will attempt to register to the callmanager and make a call.  
The call will be recorded in a file 'test.wav', which will be fed to 
Google SpeechRecognition and the transcription will be printed

##### linphone
For this code to work, linphone needs to be installed on the machine.  
We used Ubuntu, installing linphone can be done via apt / apt-get
```bash
apt-get install linphone
```
the install includes linphonec, which is a deamon version for the softphone
as well as linphonecsh, a commandline interface to the deamon

##### UCM SIP Device
for the above linphone instance to work, a proper SIP Phone will need to 
be configured on UCM. See the manuals for how to do so ... 

##### Speech Recognition
```bash
pip3 install SpeechRecognition
```
We'll be using the free Google service, so we cannot garantee the quality of 
the transcription 

##### sample output
```
$ python3 auto_dial.py
for the softphone we will need registration details
Hostname or IP of the UCM server: ucm-e*****
SIP Username: 832*****
SIP Password:
We'll also need a number that can be called for this test
Exact digits to dial: 004999*****
try to register
registered, identity=sip:832*****@ucm-e**** duration=3600
Using wav files instead of soundcard.
place call
Establishing call id to <sip:00499****@ucm-em1******>, assigned id 1
Call 1 to <sip:00499****@ucm-em*****> in progress.
unregister
test this is a test
$
```