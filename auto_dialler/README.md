this auto-dialler uses the linphone softphone to make a call.  
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

##### Speech Recognition
```bash
pip3 install SpeechRecognition
```
We'll be using the free Google service, so we cannot garantee the quality of 
the transcription 

