
from flask import Flask
from flask import request
import pyads

from objects.orchestrator import Orchestrator
from objects.conveyor import Conveyor
from objects.pallet import Pallet

plc = pyads.Connection('199.4.42.250.1.1', 851)
plc.open()
app = Flask(__name__)

conveyors = {
    1 :Conveyor(1, plc),
    2: Conveyor(2, plc),
    3: Conveyor(3, plc)
}
pallets = [Pallet(1, "Spring")]
orchestrator = Orchestrator(1, conveyors, pallets)

@app.route('/')
def hello_world():  # put application's code here
    return "Hello world"


@app.route('/conveyors/<id>', methods=['GET'])
def get_conveyor_status(id):
    try:
        id = int(id)

        if id not in conveyors.keys():
            return f'Conveyor {id} not found', 404
        else:
            result = conveyors[id].get_status()
            return result
    except ValueError:
        return "Invalid ID", 400


@app.route('/conveyors/<id>/start', methods=['POST'])
def turn_on_conveyor(id):
    try:
        id = int(id)

        if id not in conveyors.keys():
            return f'Conveyor {id} not found', 404
        else:
            conveyor = conveyors[id]
            conveyor.turn_on()
            return f'Conveyor {id} turned on', 200

    except ValueError:
        return "Invalid ID", 400


@app.route('/conveyors/<id>/stop', methods=['POST'])
def turn_off_conveyor(id):
    try:
        id = int(id)
        if id not in conveyors.keys():
            return f'Conveyor {id} not found', 404
        else:
            conveyor = conveyors[id]
            conveyor.turn_off()
            return f'Conveyor {id} turned off', 200
    except ValueError:
        return "Invalid ID", 400


@app.route('/conveyors/<id>/testLights', methods=['POST'])
def test_lights(id):
    try:
        id = int(id)
        if id in conveyors.keys():
            conveyors[id].test_lights()
            return f'Testing lights on conveyor {id}', 200
        else:
            return f'Conveyor {id} not found', 404
    except ValueError:
        return "Invalid ID", 400


@app.route('/orchestrators/<id>/testAllLights', methods=['POST'])
def test_all_lights(id):
    try:
        id = int(id)
    except ValueError:
        return "Invalid ID of orchestrator - expected number", 400

    if id != orchestrator.id:
        return "Invalid id of orchestrator - id non-existing", 400

    orchestrator.test_all_lights()
    return "Testing all lights"


@app.route('/orchestrators/<id>/collectiveTransfer', methods=['POST'])
def transfer_pallet(id):
    try:
        id = int(id)
    except ValueError:
        return "Invalid ID of orchestrator - expected number", 400

    if id != orchestrator.id:
        return "Invalid id of orchestrator - id non-existing", 400

    request_data = request.get_json()
    from_id = request_data['from']
    to_id = request_data['to']

    is_valid, msg = orchestrator.transfer_pallet(from_id, to_id)
    if is_valid:
        return f'Transfer pallet from conveyor {from_id} to {to_id} - {msg}', 200
    else:
        return msg, 400


@app.route('/conveyors/<id>/transfer', methods=['POST'])
def individual_transfer(id):
    try:
        id = int(id)
        if id in conveyors.keys():
            if conveyors[id].transfer():
                return f'Transferring pallet on conveyor {id}', 200
            else:
                return f"Invalid request - conveyor {id} is missing pallet on in_sensor", 400
        else:
            return f"Invalid conveyor id - non-existing conveyor with id {id}", 400
    except ValueError:
        return "Invalid id in request - expected number", 400


if __name__ == '__main__':
    try:
        app.run()
    finally:
        plc.close()
