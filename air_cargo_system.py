from uuid import uuid4  # Import the UUID module

class AirCargoSystem():
    def __init__(self):
        self.clients = []

    def register_client(self,client):
        self.clients.append(client)

    def do_transport(self, package):
        pass

class Client():
    def __init__(self, name):
        self.name = name
        self.id = uuid4()

class Package():
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    LOST = "Lost"

    def __init__(self, owner, origin, destination):
        self.id = uuid4()
        self.owner = owner
        self.origin = origin
        self.destination = destination
        self.status = Package.PENDING

    def set_status(self, status):
        self.status = status


if __name__ == "__main__":
    air_cargo_system = AirCargoSystem()
    client1 = Client('Ivan')
    air_cargo_system.register_client(client1)