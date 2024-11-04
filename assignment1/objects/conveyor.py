from enum import Enum
import pyads

class Status(Enum):
    OFF = 1
    IDLE = 2
    ON = 3


class Conveyor:
    def __init__(self, id, plc):
        self.plc = plc
        self.id = plc.read_by_name(f'MAIN.conv{id}.id', pyads.PLCTYPE_INT)

    def turn_on(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.is_started', True, pyads.PLCTYPE_BOOL)


    def turn_off(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.is_started', False, pyads.PLCTYPE_BOOL)

    def transfer(self):
        #todo maybe change value
        self.plc.write_by_name(f'MAIN.conv{self.id}.in_sensor', True, pyads.PLCTYPE_BOOL)

    def remove_from_conveyor(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.out_sensor', False, pyads.PLCTYPE_BOOL)

    def get_status(self):
        state = Status(self.plc.read_by_name(f'MAIN.conv{self.id}.status', pyads.PLCTYPE_INT))
        return {"id": str(self.id), "status": state.name}


    def test_lights(self):
        print("Testing lights")