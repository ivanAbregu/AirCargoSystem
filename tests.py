import pytest
from main import AirCargoSystem, Client, Package
from datetime import datetime, timedelta

USERNAME ='Ivan'

def test_create_client():
    clt = Client(USERNAME)

    assert hasattr(clt, 'username')
    assert hasattr(clt, 'packages')
    assert clt.username == USERNAME
    assert clt.packages == []

def test_register_client():
    system = AirCargoSystem()
    
    system.register_client(USERNAME)

    assert len(system.clients) == 1
    clt = next((clt for clt in system.clients if clt.username==USERNAME), None)
    assert clt is not None
    assert clt.username == USERNAME

def test_get_client_success():
    system = AirCargoSystem()

    system.register_client(USERNAME)
    system.register_client('Ciro')

    assert len(system.clients) == 2
    result = system.get_client(USERNAME)
    assert result is not None
    assert result.username == USERNAME

def test_get_client_not_found():
    system = AirCargoSystem()

    result = system.get_client('bad_username')

    assert result is None


def test_register_client_raise_excepcion():
    system = AirCargoSystem()
    system.register_client(USERNAME)

    with pytest.raises(Exception) as excinfo:
        system.register_client(USERNAME)

    assert str(excinfo.value) == "Client already register on the system"

def test_new_package():
    origin = 'Cordoba'
    destination = 'BsAs'

    pkg = Package(origin=origin, destination=destination)

    assert hasattr(pkg, 'id')
    assert hasattr(pkg, 'origin')
    assert hasattr(pkg, 'destination')
    assert hasattr(pkg, 'status')
    assert hasattr(pkg, 'cost')
    assert hasattr(pkg, 'start_date')

    assert pkg.status == Package.PENDING
    assert pkg.origin == origin
    assert pkg.destination == destination
    assert pkg.cost == 0
    assert pkg.start_date is None

def test_package_set_in_transit_raise_error_by_cost_0():
    origin = 'Cordoba'
    destination = 'BsAs'
    pkg = Package(origin, destination)

    with pytest.raises(Exception) as excinfo:
        pkg.set_in_transit()
    assert str(excinfo.value) == "The cost of delivery a package must be gretter than 0$"
    assert pkg.status == Package.PENDING

def test_do_transport_raise_error_by_not_client_registered():
    origin = 'Cordoba'
    destination = 'BsAs'
    system = AirCargoSystem()

    with pytest.raises(Exception) as excinfo:
        system.do_transport(USERNAME, origin, destination)

    assert str(excinfo.value) == f"The client {USERNAME} is not registered on the system"


def test_do_transport():
    origin = 'Cordoba'
    destination = 'BsAs'
    system = AirCargoSystem()

    system.register_client(USERNAME)
    system.do_transport(USERNAME, origin, destination)

    assert len(system.clients[0].packages) == 1

def test_get_report_by_date():
    origin = 'Cordoba'
    destination = 'BsAs'
    system = AirCargoSystem()

    system.register_client(USERNAME)
    system.register_client('Ciro')
    system.do_transport(USERNAME, origin, destination)
    system.do_transport('Ciro', origin, destination)
    res = system.get_report_by_date()
    assert res.get('amount_raised') == 20
    assert res.get('packages_count') == 2

def test_get_report_by_date_empty():
    origin = 'Cordoba'
    destination = 'BsAs'
    system = AirCargoSystem()

    # Calculate tomorrow's date
    tomorrow_date = datetime.now() + timedelta(days=1)

    system.register_client(USERNAME)
    system.do_transport(USERNAME, origin, destination)
    system.do_transport(USERNAME, origin, destination)
    
    res = system.get_report_by_date(tomorrow_date)
    assert res.get('amount_raised') == 0
    assert res.get('packages_count') == 0
