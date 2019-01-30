import json
import requests
import xmltodict
import config as cfg
from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI, SparkApiError
from axl import RawAxl

# create flask app
app = Flask(__name__)

# AXL Class
axl = RawAxl(cfg.AXL_username,cfg.AXL_password)

# init spark api
sparkapi = CiscoSparkAPI(access_token=cfg.access_token)

# get our own ID
me = sparkapi.people.me()

# check on the webhook
try:
    # find hooks
    hooks = sparkapi.webhooks.list()
    hook_ok = False
    for hook in hooks:
        if hook.targetUrl == cfg.webhook_url and hook.name == cfg.webhook_name and hook.status == 'active':
            hook_ok = True
            
    # create hook if not found
    if not hook_ok:
        sparkapi.webhooks.create(cfg.webhook_name, cfg.webhook_url, 'messages', 'created')
        print('created new hook')
            
except SparkApiError as err:
    print(err)

def user_login(userid, device, server):
    # prepare and do request
    url = 'http://{}:8080/emservice/EMServiceServlet'.format(server)
    xml = "<request><appInfo><appID>{0}</appID><appCertificate>{1}</appCertificate></appInfo><login><deviceName>{2}</deviceName><userID>{3}</userID></login></request>".format(cfg.EMAPI_username, cfg.EMAPI_password, device,userid)
    r = requests.post(url, data={'xml':xml})
    
    # process outcome
    if r.status_code is not 200:
        return False, 'Sorry, could not submit login request, contact your administrator'
    else:
        # I don't like lxml ;P
        x = xmltodict.parse(r.text)
        
        if 'failure' in x['response']:
            return False, 'Sorry, ' + x['response']['failure']['error']['#text']
        else:
            return True, 'Success, {0} is logged in into device {1}'.format(userid, device)

def user_logout(userid):
    # go over all servers and try to find logged in user
    # remark, this is ok for this PoC, ideally you should find out the server from some other
    # source (AD, telephone number management, cache, ... )
    for cluster in cfg.clusters:
        url = 'http://{}:8080/emservice/EMServiceServlet'.format(cluster[2])
        xml = "<query><appInfo><appID>{0}</appID><appCertificate>{1}</appCertificate></appInfo><userDevicesQuery><userID>{2}</userID></userDevicesQuery></query>".format(cfg.EMAPI_username, cfg.EMAPI_password, userid)
        r = requests.post(url, data={'xml':xml})
        
        cluster_outcome='{0}: {1}, '.format(cluster[0], userid)
        if r.status_code is 200:
            # we got something back
            x = xmltodict.parse(r.text)
            if 'failure' in x['response']:
                cluster_outcome += 'Sorry, ' + x['response']['failure']['error']['#text']
            elif 'doesNotExist' in x['response']['userDevicesResults']['user']:
                cluster_outcome += 'user does not exist'
            elif 'none' in x['response']['userDevicesResults']['user']:
                cluster_outcome += 'no logged in devices found for user'
            elif 'deviceName' in x['response']['userDevicesResults']['user']:
                # found it, let's try and logout
                # For our cluster, a user can only be logged in on 1 device at the time. If configured, this can return multiple devices (as a list)
                device = x['response']['userDevicesResults']['user']['deviceName']
                
                xml = "<request><appInfo><appID>{0}</appID><appCertificate>{1}</appCertificate></appInfo><logout><deviceName>{2}</deviceName></logout></request>".format(cfg.EMAPI_username, cfg.EMAPI_password, device)
                r = requests.post(url, data={'xml':xml})
                
                if r.status_code is not 200:
                    return False, 'Sorry, could not submit logout request, try again or contact your administrator'
                else:
                    x = xmltodict.parse(r.text)
                    if 'failure' in x['response']:
                        return False, 'Sorry, ' + x['response']['failure']['error']['#text']
                    else:
                        return True, 'Success, {0} is logged out from device {1}'.format(userid, device)
            else:
                cluster_outcome += 'unknown return'
        else:
            cluster_outcome += 'http error, {}'.format(r.status_code)

    # didn't find a logged in user
    return False, 'Could not find logged in user'

def find_device_by_dn(dn):
    # the dn (or part of it) is something the user will see on the screen of the phone
    # it's easier than asking for the device name, but depending on configuration of the phone
    # you may need to do some manipulation to make sure it's the dn number
    for cluster in cfg.clusters:
        axl.server = cluster[1]
        query = ("select d.name "
                    "from device as d "
                    "inner join devicenumplanmap as dmap on dmap.fkdevice=d.pkid "
                    "inner join numplan as n on dmap.fknumplan=n.pkid and n.dnorpattern = '{}' "
                    "where d.tkclass=1".format(dn))
    
        response = axl.execute('executeSQLQuery', {'sql': query})
        if response['return'] == None:
            continue
        elif len(response['return']['row']) > 1:
            print('Found multiple devices')
            devices = ''
            for dev in response['return']['row']:
                devices += dev['name']
            return False, devices, cluster[2]
        else:
            return True, response['return']['row']['name'], cluster[2]
    
    # found nothing
    return False, 'Could not find any device with that number', ''

@app.route('/', methods=['POST'])
def incoming_hook():
    spark_hook = request.json
    hook_data = spark_hook["data"]
    
    # make sure it's not us
    if hook_data["personId"] == me.id:
        return "OK"
    
    # retrieve te message and extract userid
    message = sparkapi.messages.get(hook_data['id'])
    userid = message.personEmail.split('@')[0]
    
    # say hi
    if message.text.lower() == 'hello':
        sparkapi.messages.create(roomId=message.roomId, text='Hello there')
        print('Said hi to {}'.format(userid))
        
    # what can I do
    if message.text.lower() == 'help' or message.text.lower() == 'what can you do':
        sparkapi.messages.create(roomId=message.roomId, markdown=cfg.help_message)
        print('{} asked for help'.format(userid))
    
    # try logging in
    if 'log me in into' in message.text.lower():
        words = message.text.split()
        if words[-1][0] == '8':
            #looks like a DN
            ok, text, cluster_em = find_device_by_dn(words[-1])
            if not ok:
                sparkapi.messages.create(roomId=message.roomId, text=text)
            else:
                ok, text = user_login(userid, text, cluster_em)
                sparkapi.messages.create(roomId=message.roomId, text=text)
        else:
            #if not a dn, it might be a devicename
            pass
            
    # try logging out
    if 'log me out' in message.text.lower():
        ok, text = user_logout(userid)
        sparkapi.messages.create(roomId=message.roomId, text=text)
            
    return "OK"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port='1555', threaded=True)


            