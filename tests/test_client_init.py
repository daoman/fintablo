from fintablo import FinTabloClient

def test_init():
    c = FinTabloClient(token='T')
    assert hasattr(c, 'session')
