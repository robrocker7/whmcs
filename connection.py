import urllib2
import hashlib
import json

from urllib import urlencode
import settings


class APIConn:
    url = 'http://camniomedia.com/whcms/whmcs/includes/api.php'
    username = ''
    password = ''
    responsetype = 'json'

    def __init__(self, *args, **kwargs):
        
        m = hashlib.md5()
        m.update(settings.WHMCS_PASSWORD)
        self.password = m.hexdigest()
        self.username = settings.WHMCS_USERNAME
    
    def request(self, data):
        data['username'] = self.username
        data['password'] = self.password
        data['responsetype'] = self.responsetype

        if self.url == '':
            pass #raise exception

        if 'action' not in data:
            pass #raise exception

        req = urllib2.Request(self.url, data=urlencode(data))

        resp = urllib2.urlopen(req)
        resp_data = self.parse_response(resp)

        if resp_data['result'] == 'error':
            raise APIException(resp_data['message'])
        return resp_data

    def parse_response(self, response):
        return json.loads(response.read())

class APIException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
    
