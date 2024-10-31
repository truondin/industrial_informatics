from flask import Flask

from objects.orchestrator import Orchestrator
from objects.conveyor import Conveyor
from objects.pallet import Pallet

app = Flask(__name__)

conveyors = [Conveyor(1), Conveyor(2), Conveyor(3)]
pallets = [Pallet(1, "Spring")]
orchestrator = Orchestrator(1, conveyors, pallets)

@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to conveyor system'


@app.route('/conveyors/<id>', methods=['GET'])
def get_conveyor_status(id):
    try:
        id = int(id)
        result = orchestrator.get_conveyor_status(id)
        if result is None:
            return f'Conveyor {id} not found', 404
        else:
            return result
    except ValueError:
        return "Invalid ID", 400


@app.route('/conveyors/<id>/start', methods=['POST'])
def turn_on_conveyor(id):
    try:
        id = int(id)
        if orchestrator.turn_on_conveyor(id):
            return f'Conveyor {id} turned on', 200
        else:
            return f'Conveyor {id} not turned on', 200
    except ValueError:
        return "Invalid ID", 400


@app.route('/conveyors/<id>/stop', methods=['POST'])
def turn_off_conveyor(id):
    try:
        id = int(id)
        if orchestrator.turn_off_conveyor(id):
            return f'Conveyor {id} turned off', 200
        else:
            return f'Conveyor {id} not turned off', 200
    except ValueError:
        return "Invalid ID", 400


@app.route('/pallets/<id>', methods=['GET'])
def get_pallet_info(id):
    try:
        id = int(id)
        result = orchestrator.get_pallet_info(id)
        if result is None:
            return "Pallet not found", 404
        else:
            return result
    except ValueError:
        return "Invalid ID", 400


@app.route('/lights/test/<id>', methods=['POST'])
def test_lights(id):
    try:
        id = int(id)
        if orchestrator.test_lights(id):
            return f'Testing lights on conveyor {id}', 200
        else:
            return f'Conveyor {id} not found', 404
    except ValueError:
        return "Invalid ID", 400


@app.route('/lights/test', methods=['POST'])
def test_all_lights():
    orchestrator.test_all_lights()
    return "Testing all lights"


@app.route('/transfer/<from_id>/<to_id>', methods=['POST'])
def transfer_pallet(from_id, to_id):
    try:
        from_id = int(from_id)
        to_id = int(to_id)
        if orchestrator.transfer_pallet(from_id, to_id):
            return f'Transferring pallet {from_id} to {to_id}', 200
        else:
            return "Invalid request", 400
    except ValueError:
        return "Invalid IDs", 400


if __name__ == '__main__':
    app.run()
