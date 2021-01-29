import pytest
import rdflib
import requests

from fdpclient import operations

# TODO
# - add data format tests
# - add exception tests: invalid input, not found...

# NOTE: change IP address to domain name after solving FDP server config issue
base_url = 'http://145.100.57.30/catalog'
data_url = base_url + '/catalog01'

@pytest.fixture(scope='class', autouse=True)
def setup():
    r = requests.delete(data_url)
    yield
    r = requests.delete(data_url)

class TestDefault:
    """Test fdpclient.operations functions"""

    # datadir fixture provided via pytest-datadir-ng
    def test_create(self, datadir):
        """Test create function"""
        with open(datadir['catalog01.ttl']) as f:
            data = f.read()
        r = operations.create(base_url, data=data)
        assert r is None

    def test_read(self):
        """Test read function"""
        r = operations.read(data_url)
        assert isinstance(r, rdflib.Graph)
        assert  b'hasVersion "1.0"' in r.serialize(format='turtle')

    def test_update(self, datadir):
        """Test update function"""
        with open(datadir['catalog01_update.ttl']) as f:
            data = f.read()
        r = operations.update(data_url, data=data)
        assert r is None
        r = operations.read(data_url)
        assert  b'hasVersion "2.0"' in r.serialize(format='turtle')

    def test_delete(self, capsys):
        """Test read function"""
        r = operations.delete(data_url)
        assert r is None
        with pytest.raises(RuntimeError):
            r = operations.delete(data_url)
        captured = capsys.readouterr()
        assert "HTTP error" in captured.out