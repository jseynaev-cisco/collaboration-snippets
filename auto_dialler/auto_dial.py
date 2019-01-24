import subprocess
import getpass
from time import sleep
import speech_recognition as sr


def check_call():
    audio_file = "test.wav"
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            transcription = r.recognize_google(audio)
    except sr.UnknownValueError:
        transcription = \
            " Error: Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        transcription = \
            " Error: No results from Google Speech Recognition: {}".format(e)
    except IOError:
        transcription = " Error: IO Error"
    return transcription


def register_phone(ucm_host, username, password):
    subprocess.run(['linphonecsh', 'init'])
    sleep(5)

    print('try to register')
    subprocess.run(
        ['linphonecsh', 'register',
        '--host', ucm_host,
        '--username', username,
        '--password', password])
    sleep(10)

    subprocess.run(['linphonecsh', 'status', 'register'])
    subprocess.run(['linphonecsh', 'generic', 'soundcard use files'])
    subprocess.run(['linphonecsh', "generic", "record test.wav"])


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
    subprocess.run(
        ['linphonecsh', 'dial',
         'sip:{}@ucm-em151-ams.cisco.com'.format(number_to_dial)])

    sleep(20)       # the dial command above will return immediately
    print('unregister')
    subprocess.run(['linphonecsh', 'exit'])

    print(check_call())
