from uuid import uuid4  # Import the UUID module
from datetime import datetime

class AirCargoSystem():
    PRICE = 10
    def __init__(self):
        self.clients = []

    def get_client(self, username):
        return next((clt for clt in self.clients if clt.username==username), None)

    def register_client(self,username):
        result = self.get_client(username)
        if result:
            raise Exception("Client already register on the system")
        clt = Client(username)
        self.clients.append(clt)

    def do_transport(self, username, origin, destination):
        clt = self.get_client(username)
        if(not clt):
            raise Exception(f"The client {username} is not registered on the system")

        pkg = Package(origin=origin, destination=destination)
        pkg.cost = AirCargoSystem.PRICE
        pkg.set_in_transit()
        clt.packages.append(pkg)

    def get_report_by_date(self, start_date=datetime.now()):
        result = []
        for clt in self.clients:
            result += [pkg.cost for pkg in clt.packages if pkg.start_date==start_date.date()]
        return {'packages_count':len(result), 'amount_raised':sum(result) }
class Client():
    def __init__(self, username):
        self.username = username
        self.packages = []

    def __str__(self):
        return f'username: {self.username}, packages:{len(self.packages)}'

class Package():
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    LOST = "Lost"

    def __init__(self, origin, destination):
        self.id = uuid4()
        self.cost = 0
        self.origin = origin
        self.destination = destination
        self.status = Package.PENDING
        self.start_date = None

    def set_in_transit(self):
        if(self.cost <= 0):
            raise Exception("The cost of delivery a package must be gretter than 0$")
        self.status = Package.IN_TRANSIT
        self.start_date = datetime.now().date()
