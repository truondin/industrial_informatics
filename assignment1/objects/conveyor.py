from enum import Enum


class Status(Enum):
    OFF = 0
    ON = 1
    IDLE = 2


class Conveyor:
    def __init__(self, id):
        self.id = id
        self.status = Status.OFF
        self.red_light_on = False
        self.yellow_light_on = False
        self.green_light_on = False
        self.in_sensor = False
        self.out_sensor = False
        self.motor_on = False

    def turn_on(self):
        if self.status == Status.OFF:
            self.status = Status.IDLE

    def turn_off(self):
        if self.status == Status.ON or self.status == Status.IDLE:
            self.status = Status.OFF

    def transfer_in(self):
        print("Transferring in")

    def transfer_in(self):
        print("Transferring out")

    def get_status(self):
        return {"id": str(self.id), "status": self.status.name}

    def test_lights(self):
        print("Testing lights")