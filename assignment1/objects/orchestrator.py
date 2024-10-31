
class Orchestrator:
    def __init__(self, id, conveyors, pallets):
        self.id = id
        self.conveyors = {}
        for conveyor in conveyors:
            self.conveyors[conveyor.id] = conveyor
        self.pallets = pallets
        self.valid_conveyors_transfer = [(1, 2), (2, 3), (1, 3)]

    def transfer_pallet(self, from_id, to_id):
        if (from_id, to_id) not in self.valid_conveyors_transfer:
            return False
        if from_id not in self.conveyors.keys() or to_id not in self.conveyors.keys():
            return False
        print("Transfering pallets from", from_id, "to", to_id)
        return True

    def get_conveyor_status(self, conveyor_id):
        if conveyor_id in self.conveyors:
            return self.conveyors[conveyor_id].get_status()
        else:
            return None

    def turn_on_conveyor(self, conveyor_id):
        if conveyor_id in self.conveyors:
            self.conveyors[conveyor_id].turn_on()
            return True
        return False

    def turn_off_conveyor(self, conveyor_id):
        if conveyor_id in self.conveyors:
            self.conveyors[conveyor_id].turn_off()
            return True
        return False

    def test_lights(self, conveyor_id):
        if conveyor_id in self.conveyors:
            self.conveyors[conveyor_id].test_lights()
            return True
        return False

    def test_all_lights(self):
        for conveyor in self.conveyors.values():
            conveyor.test_lights()

    def get_pallet_info(self, pallet_id):
        for pallet in self.pallets:
            if pallet.id == pallet_id:
                return pallet.get_status()
        return None