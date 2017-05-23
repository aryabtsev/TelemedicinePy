class Doctors():
    def __init__(self, id):

        self.id = id
        self.devices = set()

    def add_device(self, *args):
        self.devices.add(*args)

