class Pallet:
    def __init__(self, id, component):
        self.id = id
        self.component = component
        self.status = "STATUS"

    def get_status(self):
        return {"id": self.id, "component": self.component, "status": self.status}