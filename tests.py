import pytest
from main import AirCargoSystem, Client

def test_create_client():
    name = 'Ivan'

    clt = Client(name)

    assert clt.name == name
    assert hasattr(clt, 'id')

def test_register_client():
    name = 'Ivan'
    clt1 = Client(name)
    system = AirCargoSystem()
    
    system.register_client(clt1)

    assert len(system.clients) == 1
    clt = next((clt for clt in system.clients if clt.id==clt1.id), None)
    assert clt is not None

def test_register_client_raise_excepcion():
    name = 'Ivan'
    clt1 = Client(name)
    system = AirCargoSystem()
    
    system.register_client(clt1)
    with pytest.raises(Exception) as excinfo:
        system.register_client(clt1)
    assert str(excinfo.value) == "Client already register on the system"
