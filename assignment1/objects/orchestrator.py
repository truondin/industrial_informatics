from .conveyor import Status
import time

class Orchestrator:
    def __init__(self, id, conveyors, pallets):
        self.id = id
        self.conveyors = {}
        self.conveyors = conveyors
        self.pallets = pallets

        self.is_working = False

    def transfer_pallet(self, from_id, to_id):
        if self.is_working:
            return False, "Orchestrator is busy"

        self.is_working = True
        if from_id > to_id:
            return False, "Invalid <from> and <to> ids"

        print("Transfering pallets from", from_id, "to", to_id)
        for i in range(from_id, to_id + 1):
            print(f"iter: {i}")
            conveyor = self.conveyors[i]
            time.sleep(5)
            if conveyor.transfer():
                # todo maybe remove polling
                while conveyor.get_status()["status"] != Status.IDLE.name:
                    print(f"Conveyor {i} running")
                    time.sleep(0.5)
            else:
                self.is_working = False
                return False, f"Conveyor {i} missing pallet on in_sensor"

        self.is_working = False
        return True, "Completed"

    def get_conveyor_status(self, conveyor_id):
        print(self.conveyors.keys())
        if conveyor_id in self.conveyors.keys():
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

    def individual_transfer(self, id):
        print("Transfering pallet on conveyor", id)
        conveyor = self.conveyors[id]
        if conveyor.transfer():
            while conveyor.get_status()["status"] != Status.IDLE.name:
                print(f"Conveyor {id} running")
                time.sleep(0.5)
            return True
        else:
            return False
