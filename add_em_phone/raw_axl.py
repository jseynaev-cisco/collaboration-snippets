import sys
import json
import dicttoxml
import xmltodict
import requests

from requests.auth import HTTPBasicAuth
import urllib3


class AxlException(Exception):
    pass


class RawAxl:
    def __init__(self, username, password, server, version="10.5"):
        # setup username and password
        self.username = username
        self.password = password
        self.server = server
        self.version = version
        self.response_xml = ''

    def setCluster(self, newCluster):
        self.server = newCluster

    def execute(self, call, args, xml=''):
        # clear some stuff
        self.response_xml = ''
        # create the XML
        envelope = "<?xml version='1.0' encoding='utf8'?>"
        envelope += '<ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/" ' \
                    'xmlns:ns1="http://www.cisco.com/AXL/API/{}">'.format(self.version)
        envelope += '<ns0:Header/>'
        envelope += '<ns0:Body>'
        envelope += '<ns1:{} sequence="">'.format(call)

        # arguments from dict to xml
        if not xml == '':
            envelope += xml
        else:
            envelope += str(
                dicttoxml.dicttoxml(args, attr_type=False,
                                    root=False).decode("UTF-8"))

        # closing tags
        envelope += '</ns1:{}>'.format(call)
        envelope += '</ns0:Body>'
        envelope += '</ns0:Envelope>'

        # do the request (disable warnings)
        # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = 'https://{}:8443/axl/'.format(self.server)
        r = requests.post(
            url,
            data=envelope,
            auth=HTTPBasicAuth(self.username, self.password),
            verify=False)

        # if not 200, throw exception
        if r.status_code == 200 or r.status_code == 500:
            # ok or issue with the request (axl error), we should have a body
            # into dict and return relevant parts
            ns0 = 'http://schemas.xmlsoap.org/soap/envelope/'
            ns1 = 'http://www.cisco.com/AXL/API/{}'.format(self.version)
            #print(r.text)
            self.response_xml = r.text
            r_dict = xmltodict.parse(r.text, process_namespaces=True)
            body = r_dict['{}:Envelope'.format(ns0)]['{}:Body'.format(ns0)]

            if '{}:{}Response'.format(ns1, call) in body:
                return body['{}:{}Response'.format(ns1, call)]
            elif '{}:Fault'.format(ns0) in body:
                # clean it up a bit
                '''NOT SURE IF WE NEED THIS? CONVERTS OBJECT TO STRING.. BACK TO OBJECT. ONLY TO PRINT'''
                exceptionBody = {'fault': body['{}:Fault'.format(ns0)]}
                raise AxlException(json.loads(json.dumps(exceptionBody)))
            return body

        # not ok, the axl call didn't make it trough for some reason
        raise AxlException('Http Status {}'.format(r.status_code))


if __name__ == '__main__':
    axl = RawAxl(*sys.argv[1:])

    # print('Testcase 1:')
    # response2 = axl.execute('getPhone', {'name': "SEPxxxxxxxxxxxx"})
    # print(response2)
    # print(json.dumps(response2, sort_keys=True, indent=4))
    # print(axl.response_xml)

    # print('Testcase 2:')
    # response3 = axl.execute('addPhone', {'phone': response2['return']['phone']})
    # print(json.dumps(response3, sort_keys=True, indent=4))

    # print('Testcase 3:')
    # response = axl.execute('addAarGroup', {'aarGroup': {'name': 'testAAR'}})
    # print(response)
    # print(json.dumps(response, sort_keys=True, indent=4))

    # print('Testcase 4:')
    # response = axl.execute('getLine', {'pattern': 'xxx', 'routePartitionName': 'CORE 8Digit'})
    # print(response)
    # print(axl.response_xml)
