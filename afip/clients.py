"""
Copyright (c) 2015-2020, Hugo Osvaldo Barrera <hugo@barrera.io>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
"""
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util.ssl_ import DEFAULT_CIPHERS
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport

CIPHERS = DEFAULT_CIPHERS + "HIGH:!DH:!aNULL"
WSDLS = {
    ("wsaa", False): "https://wsaa.afip.gov.ar/ws/services/LoginCms?wsdl",
    ("wsfe", False): "https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL",
    ("wsaa", True): "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl",
    ("wsfe", True): "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL",
}


class AFIPAdapter(HTTPAdapter):
    """@author: WhyNotHugo
    An adapter with reduced security so it'll work with AFIP.
    """

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs["ssl_context"] = context
        return super().proxy_manager_for(*args, **kwargs)


def get_client(service_name: str, sandbox: bool = False) -> Client:
    key = (
        service_name.lower(),
        sandbox,
    )
    with requests.Session() as session:
        # For each WSDL, extract the domain, and add it as an exception:
        for url in WSDLS.values():
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            session.mount(base_url, AFIPAdapter())

        transport = Transport(
            cache=SqliteCache(timeout=86400), session=session
        )

        client = Client(WSDLS[key], transport=transport)
        return client
