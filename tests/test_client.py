import pytest
import rdflib
import requests

from fdpclient.client import Client

# TODO
# - add tests on fdp

base_url = 'http://example.org'
catalogID = 'catalog01'
catalog_url = base_url + '/catalog'
data_url = catalog_url + '/' + catalogID

# datadir fixture provided via pytest-datadir-ng
@pytest.fixture()
def data(datadir):
    with open(datadir['catalog01.ttl']) as f:
        return f.read()

@pytest.fixture()
def data_update(datadir):
    with open(datadir['catalog01_update.ttl']) as f:
        return f.read()

@pytest.fixture()
def client(requests_mock):
    requests_mock.get(base_url+'/fdp', status_code=200, headers={'content-type': 'text/turtle'})
    return Client(base_url)

class TestDefault:
    """Test fdpclient.client.Client methods"""

    # requests_mock fixture provided via requests-mock
    def test_create_catalog(self, client, data, requests_mock):
        """Test create_catalog method"""
        requests_mock.post(catalog_url)
        r = client.create_catalog(data=data)
        assert r is None

    def test_read_catalog(self, client, data, requests_mock):
        """Test read_catalog method"""
        requests_mock.get(data_url, text=data)
        r = client.read_catalog(catalogID)
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update_catalog(self, client, data_update, requests_mock):
        """Test update_catalog method"""
        requests_mock.put(data_url, text=data_update)
        r = client.update_catalog(catalogID, data=data_update)
        assert r is None

    def test_delete_catalog(self, client, requests_mock):
        """Test delete_catalog method"""
        requests_mock.delete(data_url)
        r = client.delete_catalog(catalogID)
        assert r is None