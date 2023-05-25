# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime
import requests
import json

_logger = logging.getLogger(__name__)

method_dict = {
    'settings': '/v2/settings'
}


class ChannelEngineApi:

    def __init__(self, host=None, api_key=None):
        self.host = host
        self.api_key = api_key

    def get_api_client(self, method_name=None):
        api_method = False
        if method_name:
            api_method = method_dict[method_name]

        full_url = str(self.host) + str(api_method) + "?api_key=" + str(self.api_key)
        response = requests.get(full_url)
        print(">>>>>>>>>>>>response", type(response), response.json())
        return response.json()
