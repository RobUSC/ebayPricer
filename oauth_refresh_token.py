import base64
import urllib

import requests
from ebaysdk.config import Config


class OAuthRefreshToken(object):

    def __init__(self, **kwargs):
        pass

    def get_token(self, **kwargs):
        self.config = Config(domain=kwargs.get('domain', 'api.ebay.com'),
                             connection_kwargs=kwargs,
                             config_file=kwargs.get('config_file', 'ebay.yaml'))
        return self.getAuthToken(self.config.get('redirecturi'), self.config.get('appid'), self.config.get('certid'))

    def getAuthToken(ru_name, app_id, cert_id):
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
