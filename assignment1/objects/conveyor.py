from enum import Enum
import pyads

class Status(Enum):
    OFF = 0
    ON = 1
    IDLE = 2


class Conveyor:
    def __init__(self, id, plc):
        self.plc = plc
        self.id = plc.read_by_name(f'conv{id}_task.conv{id}.id', pyads.PLCTYPE_INT)

    def turn_on(self):
        self.plc.write_by_name(f'conv{self.id}_task.conv{self.id}.start', True, pyads.PLCTYPE_BOOL)


    def turn_off(self):
        self.plc.write_by_name(f'conv{self.id}_task.conv{self.id}.status', Status.OFF.value, pyads.PLCTYPE_INT)

    def transfer(self):
        #todo maybe change value
        self.plc.write_by_name(f'conv{self.id}_task.conv{self.id}.in_sensor', True,pyads.PLCTYPE_BOOL)


    def get_status(self):
        state = Status(self.plc.read_by_name(f'conv{self.id}_task.conv{self.id}.status', pyads.PLCTYPE_INT))
        return {"id": str(self.id), "status": state.name}

    def test_lights(self):
        print("Testing lights")