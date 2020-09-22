# -*- coding: utf-8 -*-
import unittest

from requests.exceptions import ConnectTimeout

from yandex_checkout.client import ApiClient
from yandex_checkout.configuration import Configuration
from yandex_checkout.domain.common.http_verb import HttpVerb
from yandex_checkout.domain.common.user_agent import Version
from yandex_checkout.domain.common.request_object import RequestObject

# Requests to this URL should always fail with a connection timeout (nothing
# listening on that port)
TARPIT = "http://10.255.255.1"


class TestClient(unittest.TestCase):
    def setUp(self):
        Configuration.configure(
            account_id="test_account_id",
            secret_key="test_secret_key",
            timeout=1,
        )
        Configuration.agent_framework = Version(
            "Yandex.Money.Framework", "0.0.1"
        )
        Configuration.agent_cms = Version("Yandex.Money.Cms", "0.0.2")
        Configuration.agent_module = Version("Yandex.Money.Module", "0.0.3")
        self.client = ApiClient()
        self.client.endpoint = TARPIT

    def test_request_timout(self):
        request_args = (
            HttpVerb.GET,
            "/path",
            RequestObject(),
            {"header": "header"},
        )
        self.assertRaises(ConnectTimeout, self.client.request, *request_args)
