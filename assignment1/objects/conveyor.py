from enum import Enum
import pyads

class Status(Enum):
    OFF = 0
    ON = 1
    IDLE = 2


class Conveyor:
    def __init__(self, id, plc):
        self.plc = plc
        self.id = plc.read_by_name(f'MAIN.conv{id}.id', pyads.PLCTYPE_INT)

    def turn_on(self):
        plc.write_by_name(f'MAIN.conv{self.id}.status', Status.IDLE.value, pyads.PLCTYPE_INT)


    def turn_off(self):
        plc.write_by_name(f'MAIN.conv{self.id}.status', Status.OFF.value, pyads.PLCTYPE_INT)

    def transfer(self):
        #todo maybe change value
        plc.write_by_name(f'MAIN.conv{self.id}.start', pyads.PLCTYPE_INT)


    def get_status(self):
        state = Status(self.plc.read_by_name(f'MAIN.conv{self.id}.status', pyads.PLCTYPE_INT))
        return {"id": str(self.id), "status": state.name}

    def test_lights(self):
        print("Testing lights")