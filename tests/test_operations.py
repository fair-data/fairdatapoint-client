import pytest
import rdflib
import requests

from fdpclient import operations

# TODO
# - add data format tests
# - add exception tests: invalid input, not found...

base_url = 'http://example.org/catalog'
data_url = base_url + '/catalog01'

# datadir fixture provided via pytest-datadir-ng
@pytest.fixture()
def data(datadir):
    with open(datadir['catalog01.ttl']) as f:
        return f.read()

@pytest.fixture()
def data_update(datadir):
    with open(datadir['catalog01_update.ttl']) as f:
        return f.read()

class TestDefault:
    """Test fdpclient.operations functions"""

    # requests_mock fixture provided via requests-mock
    def test_create(self, data, requests_mock):
        """Test create function"""
        requests_mock.post(base_url)
        r = operations.create(base_url, data=data)
        assert r is None

    def test_read(self, data, requests_mock):
        """Test read function"""
        requests_mock.get(data_url, text=data)
        r = operations.read(data_url)
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update(self, data_update, requests_mock):
        """Test update function"""
        requests_mock.put(data_url)
        r = operations.update(data_url, data=data_update)
        assert r is None

    def test_delete(self, requests_mock):
        """Test read function"""
        requests_mock.delete(data_url)
        r = operations.delete(data_url)
        assert r is None