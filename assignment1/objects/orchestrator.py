from .conveyor import Status

class Orchestrator:
    def __init__(self, id, conveyors, pallets):
        self.id = id
        self.conveyors = {}
        for conveyor in conveyors:
            self.conveyors[conveyor.id] = conveyor
        self.pallets = pallets

    def transfer_pallet(self, from_id, to_id):
        if from_id > to_id:
            return False

        print("Transfering pallets from", from_id, "to", to_id)
        for i in (from_id, to_id + 1):
            conveyor = self.conveyors[i]
            conveyor.transfer()
            break
            # while conveyor.get_status()["status"] != Status.IDLE.name:
            #     print(f"Conveyor {i} waiting")

            # todo set sensor_out = False on i conveyor and set sensor_in = True on i+1 conveyor

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