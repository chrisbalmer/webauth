"""WebAUTH Class
"""
from http.client import CannotSendRequest
from http.client import HTTPSConnection
from http.client import HTTPConnection
import json
from socket import gaierror
import ssl
from time import sleep
from urllib.parse import urlparse

class WebAuth(object):
    """Represents WebAuth Process
    """

    def __init__(self,
                 url='https://1.1.1.1/login.html',
                 testurl='http://api.ipify.org/?format=json',
                 username=None,
                 password=None,
                 passthrough=True,
                 max_attempts=10):
        self.url = url
        self.testurl = testurl
        self.username = username
        self.password = password
        self.passthrough = passthrough
        self.max_attempts = max_attempts


    def authorized(self):
        """Tests the connection to see if wifi is authorized.
        """
        try:
            text = self._get_text(self.testurl)
        except NotImplementedError:
            print('Not authorized yet.')
            return False

        try:
            ipinfo = json.loads(text)
            if 'ip' in ipinfo:
                print('Already authorized.')
                return True
            else:
                print('Not authorized yet.')
                return False
        except ValueError:
            print('Not authorized yet.')
            return False


    def complete_webauth(self):
        """Performs the required WebAUTH to get access over wifi.
        """
        if self.authorized():
            return

        data = 'buttonClicked=4'
        data += '&err_flag=0'
        data += '&info_flag=0'
        data += '&info_msg='
        data += '&redirect_url='
        data += '&network_name=Guest+Network'
        data += '&err_msg='
        data += '&username={username}'.format(username=self.username)
        data += '&password={password}'.format(password=self.password)
        success = 'Login Successful'

        response = self._get_text(self.url, method='POST', body=data)

        if success in response:
            print('Authorization succeeded.')
        else:
            print('Authorization failed.')

    def _get_text(self, url, method='GET', body=None):
        """Gets the response from posting data.
        """
        url_pieces = urlparse(url)
        if url_pieces.scheme == 'https':
            context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLSv1)
            client = HTTPSConnection(url_pieces.netloc, context=context)
        else:
            client = HTTPConnection(url_pieces.netloc)

        attempts = 0
        while attempts < self.max_attempts:
            try:
                path = url_pieces.path + '?' + url_pieces.query
                client.request(method, path, body=body)
                break
            except (gaierror, CannotSendRequest):
                attempts += 1
                sleep(1)
        if attempts >= self.max_attempts:
            return ''

        with client.getresponse() as response:
            text = response.read()
        return text.decode()
