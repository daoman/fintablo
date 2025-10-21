from fintablo import FinTabloClient
from fintablo.client import _attach_endpoints

def test_settings_api_methods():
    c = FinTabloClient(token='T')
    _attach_endpoints(c)
    api = getattr(c, 'settings')
    assert callable(api.list)
    assert callable(api.get)
    assert callable(api.create)
    assert callable(api.update)
    assert callable(api.delete)
