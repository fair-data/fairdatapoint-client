import pytest
import rdflib
import requests

from fdpclient.client import Client

# TODO
# - add tests on fdp

# NOTE: change IP address to domain name after solving FDP server config issue
base_url = 'http://145.100.57.30'
catalogID = 'catalog01'
data_url = base_url + '/catalog/' + catalogID

@pytest.fixture(scope='class', autouse=True)
def client():
    r = requests.delete(data_url)
    yield Client(base_url)
    r = requests.delete(data_url)

class TestDefault:
    """Test fdpclient.operations functions"""

    # datadir fixture provided via package pytest-datadir-ng
    def test_create_catalog(self, client, datadir):
        """Test create_catalog method"""
        with open(datadir['catalog01.ttl']) as f:
            data = f.read()
        r = client.create_catalog(data=data)
        assert r is None

    def test_read_catalog(self, client):
        """Test read_catalog method"""
        r = client.read_catalog(catalogID)
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update_catalog(self, client, datadir):
        """Test update_catalog method"""
        with open(datadir['catalog01_update.ttl']) as f:
            data = f.read()
        r = client.update_catalog(catalogID, data=data)
        assert r is None
        r = client.read_catalog(catalogID)
        assert  b'hasVersion "2.0"' in r.serialize(format='turtle')

    def test_delete_catalog(self, client, capsys):
        """Test delete_catalog method"""
        r = client.delete_catalog(catalogID)
        assert r is None
        with pytest.raises(RuntimeError):
            r = client.delete_catalog(catalogID)
        captured = capsys.readouterr()
        assert "HTTP error" in captured.out