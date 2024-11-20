from enum import Enum
import pyads

class Status(Enum):
    DEFAULT = 0
    STOP = 1
    IDLE = 2
    TRANSFERRING = 3
    TESTING_LIGHTS = 4

class Conveyor:
    def __init__(self, id, plc):
        self.plc = plc
        self.id = plc.read_by_name(f'MAIN.conv{id}.id', pyads.PLCTYPE_INT)

    def turn_on(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.is_started', True, pyads.PLCTYPE_BOOL)


    def turn_off(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.is_started', False, pyads.PLCTYPE_BOOL)


    def transfer(self):
        if self.plc.read_by_name(f'MAIN.conv{self.id}.in_sensor', pyads.PLCTYPE_BOOL):
            self.plc.write_by_name(f'MAIN.conv{self.id}.transfer', True, pyads.PLCTYPE_BOOL)
            return True
        else:
            return False

    def get_status(self):
        state = Status(self.plc.read_by_name(f'MAIN.conv{self.id}.status', pyads.PLCTYPE_INT))
        return {"id": str(self.id), "status": state.name}


    def test_lights(self):
        self.plc.write_by_name(f'MAIN.conv{self.id}.test_lights', True, pyads.PLCTYPE_BOOL)
