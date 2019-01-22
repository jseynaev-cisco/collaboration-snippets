import subprocess
import getpass
from time import sleep
import speech_recognition as sr

def check_quality_score():
    AUDIO_FILE = "test.wav"
    r = sr.Recognizer()
    try:
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)
            output = r.recognize_google(audio)
    except sr.UnknownValueError:
        output = " Error: Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        output = " Error: Could not request results from Google Speech Recognition service; {}".format(e)
    except IOError:
        output = " Error: IO Error"
    return output


def register_phone(ucm_host, username, password):
    output = subprocess.run(['linphonecsh', 'init'])
    sleep(5)

    print('try to register')
    output = subprocess.run(
        ['linphonecsh', 'register',
        '--host', ucm_host,
        '--username', username,
        '--password', password])
    sleep(10)

    output = subprocess.run(['linphonecsh', 'status', 'register'])
    output = subprocess.run(['linphonecsh', 'generic', 'soundcard use files'])
    output = subprocess.run(['linphonecsh', "generic", "record test.wav"])


if __name__ == '__main__':
    # get registration details for linphone
    print("for the softphone we will need registration details")
    host = input('Hostname or IP of the UCM server: ')
    username = input('SIP Username: ')
    password = getpass.getpass('SIP Password: ')

    print("We'll also need a number that can be called for this test")
    number_to_dial = input('Exact digits to dial: ')

    register_phone(host, username, password)

    # place the call
    print('place call')
    output = subprocess.run(
        ['linphonecsh', 'dial',
         'sip:{}@ucm-em151-ams.cisco.com'.format(number_to_dial)])

    sleep(20)       # the dial command above will return immediately
    print('unregister')
    output = subprocess.run(['linphonecsh', 'exit'])

    print(check_quality_score())
