import base64
import urllib

import requests
from ebaysdk.config import Config


class OAuthRefreshToken(object):

    config = {}

    def __init__(self, **kwargs):
        pass

    @classmethod
    def get_token(cls, **kwargs):
        cls.config = Config(domain=kwargs.get('domain', 'api.ebay.com'),
                            connection_kwargs=kwargs,
                            config_file=kwargs.get('config_file', 'config/ebay.yaml'))
        return cls.getAuthToken(cls.config.get('redirecturi'), cls.config.get('appid'), cls.config.get('certid'))

    @classmethod
    def getAuthToken(cls,ru_name, app_id, cert_id):
        authHeaderData = app_id + ':' + cert_id
        encodedAuthHeader = base64.b64encode(str.encode(authHeaderData))
        encodedAuthHeader = str(encodedAuthHeader)[2:len(str(encodedAuthHeader)) - 1]

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + str(encodedAuthHeader)
        }

        body = {
            "grant_type": "client_credentials",
            "redirect_uri": ru_name,
            "scope": "https://api.ebay.com/oauth/api_scope"
        }

        data = urllib.parse.urlencode(body)

        tokenURL = "https://api.ebay.com/identity/v1/oauth2/token"

        response = requests.post(tokenURL, headers=headers, data=data)
        return response.json()
