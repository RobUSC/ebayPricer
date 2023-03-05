import uuid

from ebaysdk.config import Config
from ebaysdk.connection import HTTP_SSL
from ebaysdk.shopping import Connection
from ebaysdk import UserAgent
from requests import Request
from ebaysdk.utils import smart_encode_request_data


class OAuthShoppingConnection(Connection):

    def __init__(self, **kwargs):
        super(Connection, self).__init__(method='POST', **kwargs)

        self.config = Config(domain=kwargs.get('domain', 'open.api.ebay.com'),
                             connection_kwargs=kwargs,
                             config_file=kwargs.get('config_file', 'ebay.yaml'))

        # override yaml defaults with args sent to the constructor
        self.config.set('domain', kwargs.get('domain', 'open.api.ebay.com'))
        self.config.set('uri', '/shopping')

    def execute(self, verb, data=None, list_nodes=[], verb_attrs=None, files=None):
        self._reset()

        self._list_nodes += list_nodes
        self._add_prefix(self._list_nodes, verb)

        if hasattr(self, 'base_list_nodes'):
            self._list_nodes += self.base_list_nodes

        self.build_request(verb, data, verb_attrs, files)
        self.execute_request()

        if hasattr(self.response, 'content'):
            self.process_response()
            self.error_check()

        return self.response

    def build_request_url(self, verb):
        url = "%s://%s%s" % (
            HTTP_SSL[True],
            self.config.get('domain'),
            self.config.get('uri')
        )
        return url

    def build_request(self, verb, data, verb_attrs, token, files=None):
        self.verb = verb
        self._request_dict = data
        self._request_id = uuid.uuid4()
        self._request_id = uuid.uuid4()

        url = self.build_request_url(verb)

        headers = self.build_request_headers(verb)
        headers.update({'User-Agent': UserAgent,
                        'X-EBAY-SDK-REQUEST-ID': str(self._request_id),
                        "X-EBAY-API-IAF-TOKEN": data['token']})

        # if we are adding files, we ensure there is no Content-Type header already defined
        # otherwise Request will use the existing one which is likely not to be multipart/form-data
        # data must also be a dict so we make it so if needed

        requestData = self.build_request_data(verb, data, verb_attrs)
        if files:
            del (headers['Content-Type'])
            if isinstance(requestData, str):  # pylint: disable-msg=E0602
                requestData = {'XMLPayload': requestData}

        request = Request(self.method,
                          url,
                          data=smart_encode_request_data(requestData),
                          headers=headers,
                          files=files,
                          )

        self.request = request.prepare()
