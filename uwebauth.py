"""WebAUTH Class
"""
import time
import urequests


def authorized(url='http://api.ipify.org/?format=json'):
    """Tests the connection to see if wifi is authorized.
    """
    try:
        _ = urequests.get(url)
        return True
    except (NotImplementedError, OSError):
        print('Not authorized yet.')
        return False

def complete_webauth(url='https://1.1.1.1/login.html',
                     testurl='http://api.ipify.org/?format=json',
                     username=None,
                     password=None):
    """Performs the required WebAUTH to get access over wifi.
    """
    if authorized(testurl):
        return

    data = 'buttonClicked=4'
    data += '&err_flag=0'
    data += '&info_flag=0'
    data += '&info_msg='
    data += '&redirect_url='
    data += '&network_name=Guest+Network'
    data += '&err_msg='
    data += '&username={username}'.format(username=username)
    data += '&password={password}'.format(password=password)
    success = 'Login Successful'

    time.sleep(5)
    response = urequests.post(url, data=data)

    if success in response:
        print('Authorization succeeded.')
        return True
    else:
        print('Authorization failed.')
        return False
